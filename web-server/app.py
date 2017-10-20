from flask import Flask
import flask_restful
from pymongo import MongoClient

from resources.States import States
from resources.SignIn import SignIn
from resources.SignUp import SignUp
from resources.Devices import Devices

client = MongoClient()
db = client.zzgc  # database name: zzgc
app = Flask(__name__)

app.config["database"] = db
api = flask_restful.Api(app)

api.add_resource(SignIn, '/user/signin')
api.add_resource(SignUp, '/user/signup')
api.add_resource(States, '/states')
api.add_resource(Devices, '/device/subscribe')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
