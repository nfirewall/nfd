from .BaseResource import BaseResource
from nfd.schemata import AddressSchema
from netifaces import interfaces as list_interfaces, ifaddresses, AF_INET, AF_INET6
from flask import request
import json
import os

path = 'addresses'
endpoint = 'addresses'

class AddressResource(BaseResource):
    def get(self):
        """Get addresses of the local machine
        ---
        description: Get addresses owned by this firewall
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: AddressSchema
        """
        if not self._is_onboarded():
            return {"messages": ["Invalid request"]}, 400
        
        with open("{}masters".format(os.getenv("CONFIG_DIR")), "r") as fh:
            masters = json.load(fh)
        
        if request.remote_addr not in masters:
            return {"messages": ["Invalid request"]}, 400

        ip_list = {}
        interfaces = []
        for interface in list_interfaces():
            ip_list[interface] = []
            interfaces.append(interface)
            for link in ifaddresses(interface)[AF_INET] + ifaddresses(interface)[AF_INET6]:
                if link['addr'] not in ("127.0.0.1", "::1"):
                    ip_list[interface].append(link['addr'])
        
        return AddressSchema().dump({"interfaces": interfaces, "addresses": ip_list})