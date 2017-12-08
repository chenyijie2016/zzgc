import flask_restful as restful
from flask_restful import reqparse
from common.util import POST_HEADERS, Order
from flask import current_app
import datetime
from resources.Auth import verify_token
import time


class Devices(restful.Resource):
    def options(self):
        return {}, 200, POST_HEADERS

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('DeviceName', type=str, required=True)
        parse.add_argument('SubscribeNumber', type=int, required=True)
        parse.add_argument('token', required=True)
        args = parse.parse_args()

        db = current_app.config["database"]
        current_device = db.devices.find_one({"Name": args["DeviceName"]})
        userdb = db.user
        username = verify_token(args['token']).decode('utf8')
        #print((username))
        if not username:
            return {'ret': 401, 'message': 'token required'}

        user = userdb.find_one({'username': username})
        #print(user)
        neworder = Order.copy()
        neworder['id'] = time.time()
        neworder['device_name'] = args["DeviceName"]
        neworder['number'] = args["SubscribeNumber"]
        neworder['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        neworder['status'] = 0

        if not current_device:
            # print(404)
            return {"ret": 404, "message": "No such device"}, 200, POST_HEADERS

        if current_device["RemainingNumber"] >= args["SubscribeNumber"]:
            db.devices.update_one(
                {"Name": args["DeviceName"]},
                {"$set": {"RemainingNumber": current_device["RemainingNumber"] - args["SubscribeNumber"]}})
            user['orders'].append(neworder)
            userdb.update_one({'username': username}, {"$set": {"orders": user['orders']}})
            return {"ret": 0}, 200, POST_HEADERS
        else:

            return {"ret": 400, "message": "No enough devices"}, 200, POST_HEADERS
