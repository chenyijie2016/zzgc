import flask_restful
from common.util import *
from flask import current_app


class UserInfo(flask_restful.Resource):
    def options(self, username):
        return HEADERS

    def get(self, username):
        db = current_app.config['database']
        user = db.user.find_one({'username': username})
        del user['_id']
        del user['password']

        return user

    def post(self,username):
        db = current_app.config['database']
        user = db.user.find_one({'username': username})