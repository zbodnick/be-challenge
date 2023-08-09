from app import db
from flask import jsonify, request, session

from app.models import Lighter
from app.schemas import LighterSchema
from app.lighters import bp

# Init schema
lighter_schema = LighterSchema()
    
@bp.route('/', methods=['GET'])
def get_lighters():
    lighters = Lighter.query.all()
    result = lighter_schema.dump(lighters, many=True)
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def get_lighter(id):
    lighter = Lighter.query.get(id)
    # lighter = session.get(Lighter, id) - new method in SQLAlchemy 2.x but throwing error during testing
    if not lighter or not id:
        return jsonify({'error': 'Resource Not Found'}), 404
    
    result = lighter_schema.dump(lighter)
    return jsonify(result), 200

@bp.route('/', methods=['POST'])
def create_lighter():
    try:
        # grab request dict
        data = request.json
        # load dict into manufacturer obj
        lighter = Lighter(
            name=data['name'],
            description=data.get('description'),
            value=data.get('value'),
            image_uri=data.get('image_uri'),
            manufacturer_id=data.get('manufacturer_id'),
        )

        db.session.add(lighter)
        db.session.commit()
        return jsonify(lighter_schema.dump(lighter)), 201
    
    except Exception as e:
        return jsonify({'message': 'Error creating lighter', 'error': str(e)}), 400
    
@bp.route('/<int:id>', methods=['PATCH'])
def update_lighter(id):
    lighter = Lighter.query.get(id)
    # if not id or lighter:
    if not lighter or not id:
        return jsonify({'error': 'Resource Not Found'}), 404

    try:
        data = request.json

        for field, value in data.items():
            setattr(lighter, field, value)

        db.session.commit()
        return jsonify(lighter_schema.dump(lighter)), 201
    except Exception as e:
        return jsonify({'message': 'Error updating lighter', 'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_lighter(id):
    lighter = Lighter.query.get(id)
    if not lighter or not id:
        return jsonify({'error': 'Resource Not Found'}), 404
    
    try:
        db.session.delete(lighter)
        db.session.commit()
        return jsonify({'message': 'Lighter deleted'}), 200
    except Exception as e:
        return jsonify({'message': 'Error deleting lighter', 'error': str(e)}), 500