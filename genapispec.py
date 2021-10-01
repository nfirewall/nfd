from apispec import APISpec, BasePlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import json
from app import app
from pprint import pprint

from importlib import import_module
from nfd.schemata import submodules as schemata
from app import gen_url
from flask import Flask


from nfd.resources import submodules as resources

def gen_spec():
    app = Flask(__name__)
    with open("README.md", "r") as fh:
        readme = "".join(fh.readlines())

    spec = APISpec(
        title="nfd",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(
            description=readme,
            license=dict(
                name="MIT",
                url="https://www.mit.edu/~amini/LICENSE.md"
            ),
            contact=dict(
                name="API Support",
                url="https://github.com/nfirewall"
            )
        ),
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    for schema in schemata:
        sch = import_module("nfd.schemata.{}".format(schema))
        spec.components.schema(schema, schema=getattr(sch, schema))

    resource_views = {}
    for resource in resources:
        res = import_module("nfd.resources.{}".format(resource))
        try:
            if (res.exclude_from_doc):
                continue
        except AttributeError:
            pass
        res_view = getattr(res, resource).as_view(gen_url(res.path))
        app.add_url_rule(gen_url(res.path), view_func=res_view)
        resource_views[resource] = res_view

    with app.test_request_context():
        for resource_name in resource_views:
            spec.path(view=resource_views[resource_name])

    return spec


if __name__ == "__main__":
    spec = gen_spec()
    f = open("spec.json", "w")
    f.write(json.dumps(spec.to_dict()))
    f.close()