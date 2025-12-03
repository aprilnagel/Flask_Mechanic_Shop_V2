from app.utility.auth import mechanic_required, token_required
from . import parts_bp
from .schemas import parts_schema, part_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Parts, db, Service_Ticket_Parts

#_________________CREATE PART______________________
@parts_bp.route('', methods=['POST'])
@token_required
@mechanic_required
def create_part():
    
    if request.logged_in_role != 'mechanic':
        return jsonify({'message': 'Access forbidden: Mechanics only'}), 403
    try:
        data = part_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_part = Parts(**data)
    db.session.add(new_part)
    db.session.commit()
    return part_schema.jsonify(new_part), 201

#__________________GET ALL PARTS______________________
@parts_bp.route('', methods=['GET'])
@token_required
@mechanic_required
def get_parts():
    if request.logged_in_role != 'mechanic':
        return jsonify({'message': 'Access forbidden: Mechanics only'}), 403
    
    parts = db.session.query(Parts).all()
    return parts_schema.jsonify(parts), 200

#__________________GET PART BY ID______________________

#put part_id in the request body to get specific part. Return the part details.
@parts_bp.route('/<int:part_id>', methods=['GET'])
@token_required
@mechanic_required
def get_part_by_id(part_id):
    if request.logged_in_role != 'mechanic':
        return jsonify({'message': 'Access forbidden: Mechanics only'}), 403
    part = db.session.get(Parts, part_id)
    if not part:
        return jsonify({"message": "Part not found"}), 404
    return part_schema.jsonify(part), 200

#__________________UPDATE PART______________________
@parts_bp.route('/<int:part_id>', methods=['PUT'])
@token_required
@mechanic_required
def update_part(part_id):
    if request.logged_in_role != 'mechanic':
        return jsonify({'message': 'Access forbidden: Mechanics only'}), 403
    part = db.session.get(Parts, part_id)
    if not part:
        return jsonify({"message": "Part not found"}), 404
    try:
        data = part_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    for key, value in data.items():
        setattr(part, key, value)
    
    db.session.commit()
    return part_schema.jsonify(part), 200

#__________________DELETE PART______________________
#delete part by part_id given in the request body. return a message saying the part was deleted.
@parts_bp.route('', methods=['DELETE'])
@token_required
@mechanic_required
def delete_part():
    if request.logged_in_role != 'mechanic':
        return jsonify({'message': 'Access forbidden: Mechanics only'}), 403
    part_id = request.json.get('part_id')
    part = db.session.get(Parts, part_id)
    if not part:
        return jsonify({"message": "Part not found"}), 404
    
    #if the part is on a ticket, prevent deletion and return a message saying the part cannot be deleted because it is on a ticket
    if db.session.query(Service_Ticket_Parts).filter_by(part_id=part_id).first():
        return jsonify({"message": "Part cannot be deleted because it is associated with a service ticket"}), 400

        
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {part_id} deleted successfully"}), 200

#_________________ADD STOCK TO PART______________________
#take current part stock and add additional stock to it. return a message saying how much stock was added and the new total stock.
@parts_bp.route('/add_stock', methods=['PUT'])
@token_required
@mechanic_required
def add_stock():
    if request.logged_in_role != 'mechanic':
        return jsonify({'message': 'Access forbidden: Mechanics only'}), 403
    part_id = request.json.get('part_id')
    part = db.session.get(Parts, part_id)
    if not part:
        return jsonify({"message": "Part not found"}), 404
    try:
        data = request.json
        additional_stock = data.get('additional_stock', 0)
        if additional_stock < 0:
            return jsonify({"message": "Additional stock must be a non-negative integer"}), 400
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid input for additional stock"}), 400
    
    part.stock += additional_stock 
    db.session.commit()
    return jsonify({"message": f"Successfully added {additional_stock} to part {part_id}. New stock: {part.stock}"}), 200

    



