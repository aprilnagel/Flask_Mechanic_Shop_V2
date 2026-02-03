from app.blueprints.mechanics import mechanics_bp
from .schemas import (
    mechanic_schema,
    mechanics_schema,
    login_mechanic_schema,
    mechanic_update_schema,
    register_mechanic_schema
)
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Mechanics, mechanic_service_tickets
from werkzeug.security import generate_password_hash, check_password_hash
from app.utility.auth import encode_token, mechanic_required, token_required


# ------------------------ LOGIN ------------------------

@mechanics_bp.route('/login', methods=['POST'])
def login_mechanic():
    try:
        data = login_mechanic_schema.load(request.json)
    except ValidationError:
        return jsonify({"message": "Invalid email or password"}), 400

    mechanic = db.session.query(Mechanics).filter_by(email=data['email']).first()

    if not mechanic or not check_password_hash(mechanic.password, data['password']):
        return jsonify({"message": "Invalid email or password"}), 400

    token = encode_token(mechanic.id, 'mechanic')

    return jsonify({"token": token}), 200


# ------------------------ CREATE MECHANIC ------------------------

@mechanics_bp.route("", methods=["POST"])
def create_mechanic():
    try:
        data = register_mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check duplicates
    if db.session.query(Mechanics).filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    if db.session.query(Mechanics).filter_by(phone=data.get("phone")).first():
        return jsonify({"message": "Phone number already exists"}), 400

    hashed_pw = generate_password_hash(data["password"])

    mechanic = Mechanics(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=hashed_pw,
        phone=data.get("phone"),
        specialty=data.get("specialty"),
        role=data.get("role", "mechanic")
    )

    db.session.add(mechanic)
    db.session.commit()

    # Tests require password to be returned
    return jsonify({
        "id": mechanic.id,
        "first_name": mechanic.first_name,
        "last_name": mechanic.last_name,
        "email": mechanic.email,
        "password": mechanic.password,
        "phone": mechanic.phone,
        "specialty": mechanic.specialty,
        "role": mechanic.role
    }), 201


# ------------------------ GET ALL MECHANICS ------------------------

@mechanics_bp.route('', methods=['GET'])
@token_required
@mechanic_required
def get_mechanics():
    mechanics = db.session.query(Mechanics).all()
    if not mechanics:
        return jsonify({"message": "No mechanics found"}), 404
    return mechanics_schema.jsonify(mechanics), 200


# ------------------------ GET SINGLE MECHANIC ------------------------

@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
@token_required
@mechanic_required
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mechanic), 200


# ------------------------ DELETE MECHANIC ------------------------

@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
@token_required
@mechanic_required
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    try:
        # Remove mechanic from all assigned tickets (join table cleanup)
        db.session.execute(
            mechanic_service_tickets.delete().where(
                mechanic_service_tickets.c.mechanic_id == mechanic_id
            )
        )

        # Delete the mechanic record
        db.session.delete(mechanic)
        db.session.commit()

        return jsonify({
            "message": f"Mechanic {mechanic_id} deleted and removed from all assigned tickets."
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Error deleting mechanic:", e)
        return jsonify({"message": "Server error deleting mechanic"}), 500


# ------------------------ UPDATE MECHANIC ------------------------

@mechanics_bp.route("", methods=["PUT"])
@token_required
@mechanic_required
def update_mechanic():
    mechanic_id = request.logged_in_user_id
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    try:
        mechanic_data = mechanic_update_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in mechanic_data.items():
        if key == "password":
            value = generate_password_hash(value)
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


# ------------------------ GET MY TICKETS ------------------------

@mechanics_bp.route('/my_tickets', methods=['GET'])
@token_required
@mechanic_required
def get_my_tickets():
    from app.blueprints.Service_Tickets.schemas import service_tickets_schema
    mechanic_id = request.logged_in_user_id
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    tickets = mechanic.service_tickets_mechanics
    if not tickets:
        return jsonify({"message": "No tickets found for this mechanic"}), 404

    return service_tickets_schema.jsonify(tickets), 200


# ------------------------ GET CURRENT MECHANIC ------------------------

@mechanics_bp.route('/me', methods=['GET'])
@token_required
def get_current_mechanic():
    mechanic_id = request.logged_in_user_id
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    return mechanic_schema.jsonify(mechanic), 200


# ------------------------ LOGOUT ------------------------

@mechanics_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    return jsonify({"message": "Logout successful"}), 200