from flask import Flask, Response, send_file
import flask_restful
from pymongo import MongoClient

from resources.States import States
from resources.SignIn import SignIn
from resources.SignUp import SignUp
from resources.Devices import Devices
from resources.Record import Record
from resources.UserInfo import UserInfo

client = MongoClient()
db = client.zzgc  # database name: zzgc
app = Flask(__name__, static_url_path='')

app.config["database"] = db
app.config['SECRET_KEY'] = 'agdvvs51v5f6d1v3'
api = flask_restful.Api(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/image/<image_name>', methods=['GET'])
def image(image_name):
    if image_name == '{{device.Name}}.jpeg':
        return # 排除未渲染完成时的图片请求
    return send_file('static/image/{image_id}'.format(image_id=image_name), mimetype='image/jpeg')
    # return app.send_static_file('./image/{image_id}'.format(image_id=image_id))


api.add_resource(SignIn, '/user/signin')
api.add_resource(SignUp, '/user/signup')
api.add_resource(States, '/states')
api.add_resource(Devices, '/device/subscribe')
api.add_resource(Record, '/record/<type>')
api.add_resource(UserInfo, '/user/info/<username>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True
            # , ssl_context=('./1_chenyijie.me_bundle.crt', './2_chenyijie.me.key')
            )
