import flask_restful
from common.util import *
from flask import current_app


class States(flask_restful.Resource):
    def get(self):
        db = current_app.config["database"]
        _devices = db.devices.find().sort("Name")
        devices = []
        for device in _devices:
            devices.append({"Name": device["Name"], "Description": device["Description"],
                            "RemainingNumber": device["RemainingNumber"]})

        return devices, 200, GET_HEADERS
