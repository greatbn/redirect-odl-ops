from flask_marshmallow import Marshmallow
from marshmallow import fields
from schema.validators import validate_ip_address

ma = Marshmallow()

class HandleAttackSchema(ma.Schema):
    attacker_ip = fields.String(
        required=True, validate=validate_ip_address)
    victim_ip = fields.String(
        required=True, validate=validate_ip_address)