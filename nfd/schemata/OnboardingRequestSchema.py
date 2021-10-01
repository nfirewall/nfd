from marshmallow import fields, Schema

class OnboardingRequestSchema(Schema):
    management_key = fields.String(required=True, description="PEM of public management key")
    management_addresses = fields.List(fields.String(), required=True, description="Addresses of the management box")
    secret = fields.String(required=True, description="Pre-defined secret for onboarding")