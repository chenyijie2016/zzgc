import flask_restful
from flask_restful import reqparse
from common.util import *
from flask import current_app
import datetime
import Auth


class Record(flask_restful.Resource):
    def options(self, type):
        return {}, 200, HEADERS

    def post(self, type):
        if type == 'ip':
            parse = reqparse.RequestParser()
            parse.add_argument('ip', type=str)
            parse.add_argument('country', type=str)
            parse.add_argument('city', type=str)
            args = parse.parse_args()
            self.addip(args)

        return {}, 200, POST_HEADERS

    def get(self, type):
        parse = reqparse.RequestParser()
        parse.add_argument('token', type=str, required=True)
        args = parse.parse_args()
        if not Auth.verify_authority(args['token']):
            return {}, 403, GET_HEADERS
        data = []

        if type == 'ip':
            data = self.getip()

        return data, 200, GET_HEADERS

    def addip(self, args):
        db = current_app.config["database"]
        if not db.record.find_one({"ip": args["ip"]}):
            db.record.insert_one(
                {
                    "ip": args["ip"],
                    "country": args["country"],
                    "city": args["city"],
                    "time": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

                })
        else:
            times = db.record.find_one({"ip": args["ip"]})["time"]
            times.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.record.update({"ip": args["ip"]}, {"$set": {"time": times}})

    def getip(self):
        db = current_app.config["database"]
        ips = []
        for ip in db.record.find():
            ips.append(
                {
                    "ip": ip["ip"],
                    "time": ip["time"][-1],
                    "times": len(ip["time"]),
                    "country": ip["country"],
                    "city": ip["city"]
                })
        return ips
