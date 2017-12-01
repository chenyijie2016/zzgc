#!/usr/bin/env python
# -*- coding: utf-8 -*-     
# Copyright (c) 2017 cyj <chenyijiethu@gmail.com>
# Date: 17-8-22

import flask_restful as restful
from flask_restful import reqparse
from common.util import *
from resources.Auth import *

class SignIn(restful.Resource):
    def options():
        return {}, 200, POST_HEADERS

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str)
        parse.add_argument('password', type=str)
        parse.add_argument('token', type=str)
        args = parse.parse_args()

        if (not args["username"]) and (not args["password"]) and (not args["token"]):
            return {"ret": 401, "msg": "BAD TOKEN"}, 200, POST_HEADERS

        if args["token"]:
            if verify_token(args["token"]):
                return {"ret": 0, "msg": "TOKEN ACCEPTED, hello %s !" % verify_token(args["token"])}, 200, POST_HEADERS
            else:
                return {"ret": 403, "msg": "BAD TOKEN"}, 200, POST_HEADERS
        else:
            # print([args["username"], args["password"]])
            if verify_username_and_password(args["username"], args["password"]):
                return {"ret": 0, "msg": "SIGNIN ACCEPTED",
                        "token": generate_auth_token(username=args["username"], expires=86400)}, 200, POST_HEADERS
            else:
                return {"ret": 403, "msg": "SIGNIN FAILED"}, 200, POST_HEADERS
