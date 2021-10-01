from marshmallow import fields, Schema

class AddressSchema(Schema):
    interfaces = fields.List(fields.String(), description='Interfaces')
    addresses = fields.Dict(keys=fields.String(), values=fields.List(fields.String()), description="Interface addresses")