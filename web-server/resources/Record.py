import flask_restful
from flask_restful import reqparse
from common.util import *
from flask import current_app
import datetime


class Record(flask_restful.Resource):
    def options(self):
        return {}, 200, HEADERS

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('ip', type=str)
        parse.add_argument('country', type=str)
        parse.add_argument('city', type=str)
        args = parse.parse_args()
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

        return {}, 200, POST_HEADERS

    def get(self):
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
        print(ips)
        return ips, 200, GET_HEADERS
