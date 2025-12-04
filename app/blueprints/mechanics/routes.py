from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema, login_mechanic_schema
from app.blueprints.Service_Tickets.schemas import service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Mechanics
from werkzeug.security import generate_password_hash, check_password_hash
from app.utility.auth import encode_token, mechanic_required, token_required


#________________________#MECHANIC LOGIN ROUTE________________________

@mechanics_bp.route('/login', methods=['POST'])
# @limiter.limit("5 per 10 minutes")
 
def login_mechanic():
    try:
        data = login_mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    mechanic = db.session.query(Mechanics).filter_by(email=data['email']).first()
    
    if not mechanic or not check_password_hash(mechanic.password, data['password']):
        return jsonify({"message": "Invalid email or password"}), 400
    
    token = encode_token(mechanic.id, 'mechanic')
    
    return jsonify({
        "message": f"Welcome {mechanic.first_name} {mechanic.last_name}",
        "token": token
    }), 200


    
#_______________________#CREATE MECHANIC ROUTE________________________

@mechanics_bp.route('', methods=['POST'])
def create_mechanic():
    
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    existing_mechanic_email = db.session.query(Mechanics).filter_by(email=data['email']).first()
    if existing_mechanic_email:
        return jsonify({"message": "Email already exists"}), 400
    existing_mechanic_phone = db.session.query(Mechanics).filter_by(phone=data['phone']).first()
    if existing_mechanic_phone:
        return jsonify({"message": "Phone number already exists"}), 400
    data['password'] = generate_password_hash(data['password'])
    new_mechanic = Mechanics(**data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

  
  

#________________________#READ MECHANICS ROUTES________________________

@mechanics_bp.route('', methods=['GET'])
@token_required
@mechanic_required
def get_mechanics():
    mechanics = db.session.query(Mechanics).all()
    if request.logged_in_role != 'mechanic':
        return jsonify({'message': 'Access forbidden: Mechanics only'}), 403
    if not mechanics:
        return jsonify({"message": "No mechanics found"}), 404
    return mechanics_schema.jsonify(mechanics), 200
  

#________________________#READ A MECHANIC ROUTE________________________

@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
@token_required
@mechanic_required
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if request.logged_in_role != 'mechanic':
        return jsonify({'message': 'Access forbidden: Mechanics only'}), 403
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mechanic), 200
  
  
#________________________#DELETE A MECHANIC ROUTE________________________

@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE']) #Deleted the ID in the route so that users can only delete their own info
@token_required
@mechanic_required
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    if str(mechanic.id) != request.logged_in_user_id:
        return jsonify({"message": "You can only delete your own account"}), 403
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic deleted {mechanic_id}"}), 200
  

#________________________#UPDATE A MECHANIC ROUTE________________________

@mechanics_bp.route("", methods=["PUT"]) #No ID in the route. Users can only update their own info. Please hash passwords on update as well.
# @limiter.limit("500 per month") 
@token_required
@mechanic_required
def update_mechanic():
    mechanic_id = request.logged_in_user_id
    mechanic = db.session.get(Mechanics, mechanic_id) #Query for our mechanic to update
    
    if not mechanic: #Checking if I got a mechanic with that id
        return jsonify({"message": "Mechanic not found"}), 404
    if str(mechanic.id) != request.logged_in_user_id:
        return jsonify({"message": "You can only update your own account"}), 403
    
    #Validate and Deserialize the updates that they are sending in the body of the request
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True) #partial=True allows for partial updates
    except ValidationError as err:
        return jsonify(err.messages), 400
      
    for key, value in mechanic_data.items():
        if key == 'password':
            value = generate_password_hash(value)
        setattr(mechanic, key, value)  #Set the attribute on the mechanic instance
    
    db.session.commit() #Save the changes to the database
    return mechanic_schema.jsonify(mechanic), 200

#____________________GET MY TICKETS ROUTE____________________

@mechanics_bp.route('/my_tickets', methods=['GET'])
@token_required
@mechanic_required
def get_my_tickets():
    mechanic_id = request.logged_in_user_id #Get the mechanic ID from the token
    mechanic = db.session.get(Mechanics, mechanic_id) #Query for the mechanic
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404 #If no mechanic found, return 404
    tickets = mechanic.service_tickets_mechanics #Create a variable and show the tickets associated with that mechanic based on the relationship defined in the model. 
    if not tickets:
        return jsonify({"message": "No tickets found for this mechanic"}), 404
    return service_tickets_schema.jsonify(tickets), 200
  
  
#____________________LOGOUT ROUTE (for token-based auth, this is typically handled on the client side)____________________
@mechanics_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    return jsonify({"message": "Logout successful"}), 200