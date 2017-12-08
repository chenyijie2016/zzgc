#!/usr/bin/env python
# -*- coding: utf-8 -*-     
# Copyright (c) 2017 cyj <chenyijiethu@gmail.com>
# Date: 17-8-22

import flask_restful as restful
from flask_restful import reqparse
from common.util import POST_HEADERS,User
from flask import current_app
from werkzeug.security import generate_password_hash


class SignUp(restful.Resource):
    def options(self):
        return {}, 200, POST_HEADERS

    def post(self):
        db = current_app.config["database"]  # database name: zzgc
        collection = db.user  # collection name: user
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str)
        parse.add_argument('password', type=str)
        parse.add_argument('email', type=str)

        args = parse.parse_args()

        if args["username"] is None or args["password"] is None or args["email"] is None:
            return {"ret": 400, "msg": "incomplete request"}, 200, POST_HEADERS

        query = collection.find_one({"username": args["username"]})

        if query is not None:
            return {"ret": 400, "msg": "username already exists"}, 200, POST_HEADERS

        newuser = User.copy()

        newuser['username']=args["username"]
        newuser['password']=generate_password_hash(args["password"])
        newuser['email']=args["email"]
        newuser['authority'] = 'user'

        collection.insert_one(newuser)

        return {"ret": 0, "msg": "create a new user"}, 200, POST_HEADERS
