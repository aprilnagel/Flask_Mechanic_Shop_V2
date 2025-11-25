from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema, login_customer_schema
from app.blueprints.Service_Tickets.schemas import service_tickets_schema
from app.utility.auth import customer_required, encode_token, mechanic_required, token_required
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash

#____________________CUSTOMER LOGIN ROUTE____________________

@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_customer_schema.load(request.json) #JSON > Python
    except ValidationError as err:
        return jsonify(err.messages), 400 #return the error messages and a 400 status code if validation fails
    
    customer = db.session.query(Customers).where(Customers.email == data['email']).first()

    if customer and check_password_hash(customer.password, data['password']):
        #create token for customer
        token = encode_token(customer.id, role='customer')
        return jsonify({
            "message": f"Welcome {customer.first_name} {customer.last_name}",
            "token": token,
        }), 200
    return jsonify({"message": "Invalid email or password"}), 401


#____________________________CREATE CUSTOMER ROUTE____________________________

@customers_bp.route("",methods=['POST'])
# @limiter.limit("200 per day")
def create_customer():
    try:
        data = customer_schema.load(request.json) #JSON > Python
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    data['password'] = generate_password_hash(data['password'])
    #create a new customer instance
    new_customer = Customers(**data) #Unpack the data dictionary into the Customer model
    
    db.session.add(new_customer)
    
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


#____________________________READ ALL CUSTOMERS ROUTE____________________________
#read all customers. Only mechanics can see all customers. 
@customers_bp.route("", methods=['GET'])
@token_required
@mechanic_required
def get_customers():
    customers = db.session.query(Customers).all()
    return customers_schema.jsonify(customers), 200


#____________________________READ A SINGLE CUSTOMER ROUTE____________________________

@customers_bp.route('/<int:customer_id>', methods=['GET'])
@token_required
def get_customer(customer_id):
    # Query by primary key
    customer = db.session.get(Customers, customer_id)

    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    if str(customer.id) != request.logged_in_user_id:
        return jsonify({'message': 'Access forbidden: You can only view your own customer data'}), 403
        
    response = {
        'id': customer.id,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address,  
        'role': customer.role
    }
    return jsonify(response), 200
   
#____________________________DELETE CUSTOMER ROUTE____________________________

@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@token_required
@customer_required
def delete_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    if str(customer.id) != request.logged_in_user_id:
        return jsonify({"message": "You can only delete your own account"}), 403
    
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer deleted {customer_id}"}), 200


#____________________________UPDATE CUSTOMER ROUTE____________________________

@customers_bp.route('/<int:customer_id>', methods=["PUT"])
@token_required
@customer_required
def update_customer(customer_id):
    #Query the customer by id
    customer = db.session.get(Customers, customer_id) #Query for our customer to update
    if not customer: #Checking if I got a customer with that id
        return jsonify({"message": "Customer not found"}), 404 
    if str(customer.id) != request.logged_in_user_id:
        return jsonify({"message": "You can only update your own account"}), 403
    #Validate and Deserialize the updates that they are sending in the body of the request
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    # for each of the values that they are sending, we will change the value of the queried object
    
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    
    db.session.commit() #Save the changes to the database
    return customer_schema.jsonify(customer), 200

#__________________________GET MY SERVICE TICKETS ROUTE____________________________

@customers_bp.route('/my_tickets', methods=['GET'])
@token_required
@customer_required
def get_my_tickets():
    customer_id = request.logged_in_user_id #Get the customer ID from the token
    customer = db.session.get(Customers, customer_id) #Query for the customer
    if not customer:
        return jsonify({"message": "Customer not found"}), 404 #If no customer found, return 404
    if str(customer.id) != request.logged_in_user_id:
        return jsonify({"message": "You can only view your own tickets"}), 403
    
    tickets = customer.service_tickets_customer
    if not tickets:
        return jsonify({"message": "No service tickets found"}), 404
    
    
    return service_tickets_schema.jsonify(tickets), 200
