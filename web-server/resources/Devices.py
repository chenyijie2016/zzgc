import flask_restful as restful
from flask_restful import reqparse
from common.util import POST_HEADERS
from flask import current_app


class Devices(restful.Resource):
    def options(self):
        return {}, 200, POST_HEADERS

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('DeviceName', type=str, required=True)
        parse.add_argument('SubscribeNumber', type=int, required=True)
        args = parse.parse_args()

        db = current_app.config["database"]
        current_device = db.devices.find_one({"Name": args["DeviceName"]})
        if not current_device:
            # print(404)
            return {"ret": 404, "message": "No such device"}, 200, POST_HEADERS

        if current_device["RemainingNumber"] >= args["SubscribeNumber"]:
            db.devices.update_one(
                {"Name": args["DeviceName"]},
                {"$set": {"RemainingNumber": current_device["RemainingNumber"] - args["SubscribeNumber"]}})
            # print(0)
            return {"ret": 0}, 200, POST_HEADERS
        else:
            # print(400)
            return {"ret": 400, "message": "No enough devices"}, 200, POST_HEADERS
