from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, Mechanics, db, Service_Tickets, Parts, Service_Ticket_Parts
from app.extensions import limiter, cache


#__________________CREATE SERVICE TICKET ROUTE____________________#

@service_tickets_bp.route('', methods=['POST'])

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
@cache.cached(timeout=30)
def get_service_tickets():
    service_tickets = db.session.query(Service_Tickets).all()
    return service_tickets_schema.jsonify(service_tickets), 200


#____________________________READ A SINGLE SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    return service_ticket_schema.jsonify(service_ticket), 200


#____________________________DELETE SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Service Ticket deleted {service_ticket_id}"}), 200


#____________________________UPDATE SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route("/<int:service_ticket_id>", methods=["PUT"])
# @limiter.limit("5 per day")
def update_service_ticket(service_ticket_id):
    
    #Query the service ticket by id
    service_ticket = db.session.get(Service_Tickets, service_ticket_id) #Query for our service ticket to update
    if not service_ticket: #Checking if I got a service ticket with that id
        return jsonify({"message": "Service Ticket not found"}), 404 
    #Validate and Deserialize the updates that they are sending in the body of the request
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    # for each of the values that they are sending, we will change the value of the queried object
    
    # if service_ticket_data['description']:
    #   service_ticket.description = service_ticket_data["description"]

    for key, value in service_ticket_data.items():
        setattr(service_ticket, key, value)
        
    # commit the changes
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200


#____________________________ASSIGN MECHANIC TO SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/<int:service_ticket_id>/assign_mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic_to_service_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    service_ticket.mechanics_service_tickets.append(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(service_ticket), 200


#____________________________REMOVE MECHANIC FROM SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic_from_service_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    service_ticket.mechanics_service_tickets.remove(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(service_ticket), 200


#_________________ADD PART TO SERVICE TICKET______________________
@service_tickets_bp.route('/<int:service_ticket_id>/add_part', methods=['PUT'])
def add_part_to_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    #enter part id and quantity in the request body
    part = db.session.get(Parts, request.json.get('part_id'))
    if not part:
        return jsonify({"message": "Part not found"}), 404
    quantity = request.json.get('quantity', 1)
    if quantity <= 0:
        return jsonify({"message": "Quantity must be greater than zero"}), 400
    
    #subtract the part quantity from the part stock in the parts table
    if part.stock < quantity:
        return jsonify({"message": "Insufficient stock for the requested part"}), 400
    part.stock -= quantity
    
    #add parts and price to the service ticket
    if service_ticket.parts:
        service_ticket.parts += f", {part.part_name} (x{quantity})"
    else:
        service_ticket.parts = f"{part.part_name} (x{quantity})"
    
    service_ticket.price = (service_ticket.price or 0) + (part.price * quantity)
    
       
    #create a new service ticket parts association object
    service_ticket_part = Service_Ticket_Parts(service_ticket_id=service_ticket.id, part_id=part.id, quantity=quantity)
    db.session.add(service_ticket_part)
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

#_________________REMOVE PART FROM SERVICE TICKET______________________
@service_tickets_bp.route('/<int:service_ticket_id>/remove_part', methods=['PUT'])
def remove_part_from_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    part = db.session.get(Parts, request.json.get('part_id'))
    if not part:
        return jsonify({"message": "Part not found"}), 404
    
    service_ticket_part = db.session.query(Service_Ticket_Parts).filter_by(service_ticket_id=service_ticket.id, part_id=part.id).first()
    if not service_ticket_part:
        return jsonify({"message": "Part not associated with this Service Ticket"}), 404
    
    quantity = db.session.get(Service_Ticket_Parts, service_ticket_part.id).quantity
    
    #add the part quantity back to the part stock in the parts table
    part.stock += quantity
    
    #Remove the parts and price from the service ticket. The price MUST match the quantity being removed and existing ticket quantity can't be < 1
    HELP
    if service_ticket.parts:
        parts_list = service_ticket.parts.split(", ")
        part_entry = f"{part.part_name} (x{quantity})"
        
        if part_entry in parts_list:
            parts_list.remove(part_entry)
            service_ticket.parts = ", ".join(parts_list) if parts_list else None
    service_ticket.price = (service_ticket.price or 0) - (part.price * quantity)
    if service_ticket.price < 0:
        service_ticket.price = 0    
   
        
    db.session.delete(service_ticket_part)
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

