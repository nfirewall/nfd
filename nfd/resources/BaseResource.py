from flask.views import MethodView
from flask import request
import os

class BaseResource(MethodView):
    _allowed_content_types = ['application/json']

    def dispatch_request(self, *args, **kwargs):
        if not self._check_method():
            return "Invalid Content-Type", 400
        return super(BaseResource, self).dispatch_request(*args, **kwargs)

    def _check_method(self):
        meth = request.method.lower()
        if meth in ['get', 'head', 'delete']:
            return True
        if request.content_type in self._allowed_content_types:
            return True
        return False
    
    def _is_onboarded(self):
        if os.path.exists("{}sercret.txt".format(os.getenv("CONFIG_DIR"))):
            return False
        if not os.path.exists("{}masters".format(os.getenv("CONFIG_DIR"))) or not os.path.exists("{}management.crt".format(os.getenv("CONFIG_DIR"))):
            return False
        return True