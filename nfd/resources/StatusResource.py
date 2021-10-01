from .BaseResource import BaseResource
import socket

path = 'status'
endpoint = 'status'


class StatusResource(BaseResource):
    def get(self):
        """Get nfd status
        ---
        description: Get status of the nfirewall daemon
        responses:
          200:
            content:
              application/json:
                schema: StatusSchema
        """

        return {
            "version": "0.1",
            "hostname": socket.gethostname()
        }