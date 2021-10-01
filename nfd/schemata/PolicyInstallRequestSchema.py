from marshmallow import fields, Schema

class PolicyInstallRequestSchema(Schema):
    policy = fields.String(required=True, description='Base64 encoded policy')
    signature = fields.String(required=True, description='Base64 encoded signature')