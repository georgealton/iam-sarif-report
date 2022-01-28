import json

import pkg_resources


checks_fp = pkg_resources.resource_stream(__name__, "checks.json")
checks = json.load(checks_fp)
