from marshmallow import Schema, fields, validate, ValidationError

class ManufacturerSchema(Schema):
    # dump_only=True to prevent client side id input
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    image_uri = fields.URL(required=True)

class LighterSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    name = fields.String(required=True)
    value = fields.Float(required=True)
    description = fields.String(required=True)
    image_uri = fields.URL(required=True)
    manufacturer_id = fields.Integer(required=True)