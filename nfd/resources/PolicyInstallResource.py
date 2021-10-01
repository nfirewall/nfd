from flask import request
from marshmallow.exceptions import ValidationError
from flask.views import MethodView
from ..schemata import PolicyInstallRequestSchema
import os
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import base64

path = 'policy_install'
endpoint = 'policy_install'

class PolicyInstallResource(MethodView):
    def post(self):
        """Install a policy package
        ---
        description: Install a policy package
        requestBody:
          content:
            application/json:
              schema: PolicyInstallRequestSchema
        responses:
          200:
            description: Ok
            content:
              application/json:
                schema: MessageSchema
          400:
            description: Bad request
            content:
              application/json:
                schema: MessageSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()
        try:
            data = PolicyInstallRequestSchema().load(json_data)
        except ValidationError as err:
            messages = []
            for msg in err.messages:
                messages.append("{}: {}".format(msg, ":".join(err.messages[msg])))
            return messages, 422
        policy = base64.b64decode(data["policy"])
        signature = base64.b64decode(data["signature"])


        with open("{}/management.pem".format(os.getenv("CONFIG_DIR")), "r") as fh:
            pem = "".join(fh.readlines())
        key = serialization.load_pem_public_key(pem.encode("utf-8"))

        try:
            key.verify(signature=signature, data=policy, signature_algorithm=ec.ECDSA(hashes.SHA256()))
        except InvalidSignature:
            return {"messages": ["Invalid signature"]}, 400
        
        print("Ok to install!")