#!/usr/bin/env python
# -*- coding: utf-8 -*-     
# Copyright (c) 2017 cyj <chenyijiethu@gmail.com>
# Date: 17-8-25
from flask import current_app
from werkzeug.security import check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


def verify_username_and_password(username, password):
    db = current_app.config["database"]
    collection = db.user  # collection name: user
    user = collection.find_one({"username": username})
    if not user:
        return False
    else:
        return check_password_hash(user["password"], password)


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        s.loads(token)
    except SignatureExpired:
        return False

    except BadSignature:
        return False
    return s.loads(token)["username"].encode('utf-8')


def generate_auth_token(username, expires=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires)
    return s.dumps({'username': username}).decode('utf-8')


def verify_authority(token, identity='admin'):
    username = verify_token(token)
    db = current_app.config["database"]
    if username:
        user = db.user.find_one({"username": str(username, encoding='utf-8')})
        if user:
            return user["authority"] == identity
        else:
            return False
    return False
