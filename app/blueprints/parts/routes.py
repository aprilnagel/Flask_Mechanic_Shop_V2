from . import parts_bp
from .schemas import parts_schema, part_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Parts, db

#_________________CREATE PART______________________
@parts_bp.route('', methods=['POST'])
def create_part():
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
def get_parts():
    parts = db.session.query(Parts).all()
    return parts_schema.jsonify(parts), 200

#__________________GET PART BY ID______________________

@parts_bp.route('/<int:part_id>', methods=['GET'])
def get_part(part_id):
    part = db.session.get(Parts, part_id)
    return part_schema.jsonify(part), 200

#__________________UPDATE PART______________________
@parts_bp.route('/<int:part_id>', methods=['PUT'])
def update_part(part_id):
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
@parts_bp.route('/<int:part_id>', methods=['DELETE'])
def delete_part(part_id):
    part = db.session.get(Parts, part_id)
    if not part:
        return jsonify({"message": "Part not found"}), 404
    
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted part {part_id}"}), 200

#_________________ADD STOCK TO PART______________________
#take current part stock and add additional stock to it. return a message saying how much stock was added and the new total stock.
@parts_bp.route('/<int:part_id>/add_stock', methods=['PUT'])
def add_stock(part_id):
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
    return jsonify({"message": f"Successfully added {additional_stock} to part {[part_id]}. New stock: {part.stock}"}), 200

    



