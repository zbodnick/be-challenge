from app import db
from flask import jsonify, request

from app.models import Manufacturer
from app.schemas import ManufacturerSchema
from app.manufacturers import bp

# Init schemas
manufacturer_schema = ManufacturerSchema()

@bp.route('/', methods=['GET'])
def get_manufacturers():
    manufacturers = Manufacturer.query.all()
    result = manufacturer_schema.dump(manufacturers, many=True)
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def manufacturer(id):
    manufacturer = Manufacturer.query.get(id)
    if not manufacturer or not id:
        return jsonify({'error': 'Resource Not Found'}), 404
    
    result = manufacturer_schema.dump(manufacturer)
    return jsonify(result), 200

@bp.route('/', methods=['POST'])
def create_manufacturer():
    try:
        # grab request dict
        data = request.json
        # load dict into manufacturer obj
        manufacturer = Manufacturer(
            name=data['name'],
            description=data.get('description'),
            image_uri=data.get('image_uri')
        )

        db.session.add(manufacturer)
        db.session.commit()
        return jsonify(manufacturer_schema.dump(manufacturer)), 201
    except Exception as e:
        return jsonify({'message': 'Error creating manufacturer', 'error': str(e)}), 400
    
@bp.route('/<int:id>', methods=['PATCH'])
def update_manufacturer(id):
    manufacturer = Manufacturer.query.get(id)
    if not manufacturer or not id:
        return jsonify({'error': 'Resource Not Found'}), 404

    try:
        data = request.json

        # Update corresponding fields in the manufacturer
        for field, value in data.items():
            setattr(manufacturer, field, value)

        db.session.commit()
        return jsonify(manufacturer_schema.dump(manufacturer)), 201
    
    except Exception as e:
        return jsonify({'message': 'Error updating manufacturer', 'error': str(e)}), 400
    
@bp.route('/<int:id>', methods=['DELETE'])
def delete_manufacturer(id):
    manufacturer = Manufacturer.query.get(id)
    if not manufacturer or not id:
        return jsonify({'error': 'Resource Not Found'}), 404

    try:
        db.session.delete(manufacturer)
        db.session.commit()
        return jsonify({'message': 'Manufacturer deleted'})
    except Exception as e:
        return jsonify({'message': 'Error deleting manufacturer', 'error': str(e)}), 500