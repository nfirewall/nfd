from marshmallow import fields, Schema

class StatusSchema(Schema):
    version = fields.String(description='Software Version')
    hostname = fields.String(description='Firewall Hostname')