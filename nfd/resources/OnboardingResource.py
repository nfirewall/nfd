from .BaseResource import BaseResource
from flask import request
from nfd.schemata import OnboardingRequestSchema
from marshmallow.exceptions import ValidationError
import json
import os

path = 'onboarding'
endpoint = 'onboarding'


class OnboardingResource(BaseResource):
    def post(self):
        """Onboard into management
        ---
        description: Onboard this firewall to nfirewall management
        requestBody:
          content:
            application/json:
              schema: OnboardingRequestSchema
        responses:
          200:
            description: Onboarded
            content:
              application/json:
                schema:
                  items: MessageSchema
          422:
            description: Failed
            content:
              application/json:
                schema:
                  items MessageSchema
        """
        config_path = os.getenv("CONFIG_DIR")
        json_data = request.get_json()
        try:
            data = OnboardingRequestSchema().load(json_data)
        except ValidationError as err:
            messages = []
            for msg in err.messages:
                messages.append("{}: {}".format(msg, err.messages[msg]))
            return {"messages": messages}, 422
        
        management_key = data["management_key"]
        management_addresses = data["management_addresses"]
        secret = data["secret"]

        try:
            with open("{}secret.txt".format(config_path), "r") as fh:
                stored_secret = fh.readlines()[0].strip()
        except FileNotFoundError:
            print("Can't find the file")
            return {"messages": ["invalid shared secret specified"]}, 401

        if stored_secret != secret:
            print("Invalid shared secret {} vs {}".format(stored_secret, secret))
            return {"messages": ["invalid shared secret specified"]}, 401

        os.remove("{}secret.txt".format(config_path))

        with open("{}management.key".format(config_path), "w") as fh:
            fh.write(management_key)
        
        with open("{}masters".format(config_path), "w") as fh:
            fh.write(json.dumps(management_addresses))
        
        return {"messages": ["OK"]}