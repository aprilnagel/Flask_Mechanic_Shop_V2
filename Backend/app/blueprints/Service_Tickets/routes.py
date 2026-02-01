from app.utility.auth import mechanic_required, token_required
from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, Mechanics, db, Service_Tickets, Parts, Service_Ticket_Parts
from app.extensions import limiter, cache


#__________________CREATE SERVICE TICKET ROUTE____________________#

@service_tickets_bp.route('', methods=['POST'])
@token_required
@mechanic_required

def create_service_ticket():
    #Validate and Deserialize the data
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    #Create a new Service Ticket object
    new_service_ticket = Service_Tickets(**service_ticket_data)
    
    #Add to the database
    db.session.add(new_service_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_service_ticket), 201


#__________________READ SERVICE TICKETS ROUTE____________________#

@service_tickets_bp.route('', methods=['GET'])
@token_required
@mechanic_required
@cache.cached(timeout=30)
def get_service_tickets():
    service_tickets = db.session.query(Service_Tickets).all()
    return service_tickets_schema.jsonify(service_tickets), 200


#____________________________READ A SINGLE SERVICE TICKET ROUTE____________________________#

#read a single service ticket but customers can only see their own tickets
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
@token_required
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    if request.logged_in_role == 'mechanic':
        pass  # Mechanics can access all tickets
    #If the logged in user is a customer, ensure they can only access their own tickets
    if request.logged_in_role == 'customer':
        if service_ticket.customer_id != int(request.logged_in_user_id):
            return jsonify({"message": "Access denied: You can only view your own service tickets."}), 403
    
    return service_ticket_schema.jsonify(service_ticket), 200


#____________________________DELETE SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('', methods=['DELETE'])
@token_required
@mechanic_required
def delete_service_ticket():
    service_ticket = db.session.get(Service_Tickets, request.json.get('service_ticket_id'))
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Service Ticket deleted {request.json.get('service_ticket_id')}"}), 200


#____________________________UPDATE SERVICE TICKET ROUTE____________________________#

#update a service ticket by querying by id
@service_tickets_bp.route('', methods=['PUT'])
@token_required
@mechanic_required
def update_service_ticket():
    service_ticket = db.session.get(Service_Tickets, request.json.get('service_ticket_id'))
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    #Update fields
    for key, value in request.json.items():
        if key != 'service_ticket_id' and hasattr(service_ticket, key):
            setattr(service_ticket, key, value)
    #If status is being updated to "Complete", set the completion_date to today
    if 'status' in request.json and request.json['status'] == "Complete":
        from datetime import date
        service_ticket.completion_date = date.today()
    
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200


#____________________________ASSIGN MECHANIC TO SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/assign_mechanic/', methods=['PUT'])
@token_required
@mechanic_required
def assign_mechanic_to_service_ticket():
    # 1. Query service ticket by ID
    service_ticket_id = request.json.get('service_ticket_id')
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404

    # 2. Query mechanic by ID
    mechanic_id = request.json.get('mechanic_id')
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    # 3. Prevent duplicate assignment
    if mechanic in service_ticket.mechanics_service_tickets:
        return jsonify({"message": f"Mechanic {mechanic.id} is already assigned to Service Ticket {service_ticket.id}."}), 400

    # 4. Add mechanic to service ticket
    service_ticket.mechanics_service_tickets.append(mechanic)

    # 5. Update status to "In Progress"
    service_ticket.status = "In Progress"

    # 6. Confirmation message
    confirmation_message = (
        f"Mechanic {mechanic.id}, {mechanic.first_name} {mechanic.last_name} assigned to Service Ticket {service_ticket.id}. "
        f"Status set to In Progress."
    )

    # 7. Commit changes and return updated ticket
    db.session.commit()
    response = service_ticket_schema.dump(service_ticket)
    response["confirmation"] = confirmation_message

    return jsonify(response), 200



#____________________________REMOVE MECHANIC FROM SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/remove_mechanic/', methods=['PUT'])
@token_required
@mechanic_required
def remove_mechanic_from_service_ticket():
    # 1. Query service ticket by ID
    service_ticket_id = request.json.get('service_ticket_id')
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404

    # 2. Query mechanic by ID
    mechanic_id = request.json.get('mechanic_id')
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    # 3. Check if mechanic is assigned
    if mechanic not in service_ticket.mechanics_service_tickets:
        return jsonify({"message": f"Mechanic {mechanic.id} is not assigned to Service Ticket {service_ticket.id}."}), 400

    # 4. Remove mechanic from service ticket
    service_ticket.mechanics_service_tickets.remove(mechanic)

    # 5. Update status if no mechanics remain
    if not service_ticket.mechanics_service_tickets:
        service_ticket.status = "Pending"  # or "Open" depending on your workflow

    # 6. Confirmation message
    confirmation_message = (
        f"Mechanic {mechanic.id}, {mechanic.first_name} {mechanic.last_name} removed from Service Ticket {service_ticket.id}."
        f" Current status: {service_ticket.status}."
    )

    # 7. Commit changes and return updated ticket
    db.session.commit()
    response = service_ticket_schema.dump(service_ticket)
    response["confirmation"] = confirmation_message

    return jsonify(response), 200


#_________________ADD PART TO SERVICE TICKET______________________

#we will need to query the service ticket to see of the part already exists. If it does, we will just update the quantity and price. We will not create a duplicate entry in the service ticket parts association table. Then we will subtract the part quantity from the parts stock in the parts table and update the service ticket price accordingly.

@service_tickets_bp.route('/add_part', methods=['PUT'])
@token_required
@mechanic_required
def add_part_to_service_ticket():
    # Get service ticket
    service_ticket = db.session.get(Service_Tickets, request.json.get('service_ticket_id'))
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404

    # Get part
    part = db.session.get(Parts, request.json.get('part_id'))
    if not part:
        return jsonify({"message": "Part not found"}), 404

    # Validate quantity
    quantity = request.json.get('quantity', 1)
    if quantity is None or quantity <= 0:
        return jsonify({"message": "Quantity must be greater than zero"}), 400
    if part.stock < quantity:
        return jsonify({"message": "Insufficient stock for the requested part"}), 400

    # Check if part already exists in the service ticket
    service_ticket_part = db.session.query(Service_Ticket_Parts).filter_by(service_ticket_id=service_ticket.id, part_id=part.id).first()

    if service_ticket_part:
        # Update quantity
        service_ticket_part.quantity += quantity
    else:
        # Create new association
        service_ticket_part = Service_Ticket_Parts(service_ticket_id=service_ticket.id, part_id=part.id, quantity=quantity)
        db.session.add(service_ticket_part)

    # Update stock
    part.stock -= quantity

    # Update price (initialize if None)
    if service_ticket.price is None:
        service_ticket.price = 0.0
    service_ticket.price += (part.price * quantity)

    # Regenerate the parts field from the association table
    service_ticket.parts = ", ".join(
        f"{p.part.part_name} (x{p.quantity})"
        for p in db.session.query(Service_Ticket_Parts).filter_by(service_ticket_id=service_ticket.id).all()
    )
    
    confirmation_message = f"Added {quantity} x {part.part_name} to Service Ticket {service_ticket.id}."

     # Commit all changes

    db.session.commit()
    response = service_ticket_schema.dump(service_ticket)
    response["confirmation"] = confirmation_message
    return jsonify(response), 200
    

#_________________REMOVE PART FROM SERVICE TICKET______________________

@service_tickets_bp.route('/remove_part', methods=['PUT'])
@token_required
@mechanic_required
def remove_part_from_service_ticket():
    # Get service ticket
    service_ticket = db.session.get(Service_Tickets, request.json.get('service_ticket_id'))
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404

    # Get part
    part = db.session.get(Parts, request.json.get('part_id'))
    if not part:
        return jsonify({"message": "Part not found"}), 404

    # Validate quantity
    quantity = request.json.get('quantity', 1)
    if quantity is None or quantity <= 0:
        return jsonify({"message": "Quantity must be greater than zero"}), 400

    # Check if part exists in the service ticket
    service_ticket_part = db.session.query(Service_Ticket_Parts).filter_by(service_ticket_id=service_ticket.id,part_id=part.id).first()

    if not service_ticket_part:
        return jsonify({"message": "Part not found on this Service Ticket"}), 404

    # Ensure we don't remove more than exists
    if service_ticket_part.quantity < quantity:
        return jsonify({"message": "Cannot remove more parts than are on the ticket"}), 400

    
    
    # Update or delete association
    service_ticket_part.quantity -= quantity
    if service_ticket_part.quantity == 0:
        db.session.delete(service_ticket_part)

    # Restore stock
    part.stock += quantity

    # Update price (initialize if None)
    if service_ticket.price is None:
        service_ticket.price = 0.0
    service_ticket.price -= (part.price * quantity)
    if service_ticket.price < 0:
        service_ticket.price = 0.0  # safety guard

    # Regenerate the parts field from association table
    service_ticket.parts = ", ".join(
        f"{p.part.part_name} (x{p.quantity})"
        for p in db.session.query(Service_Ticket_Parts).filter_by(service_ticket_id=service_ticket.id).all()
    )
    
    confirmation_message = f"Removed {quantity} x {part.part_name} from Service Ticket {service_ticket.id}."

    db.session.commit()
    
    response = service_ticket_schema.dump(service_ticket)
    response["confirmation"] = confirmation_message

    return jsonify(response), 200


    
    
 


