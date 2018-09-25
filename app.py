from flask import Flask
from flask_restful import Api
from resources.Hello import Hello
from models.models import Model
from models.train import Train
from flask import request
import json

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

# api.add_resource(Model, '/test_app/<string:number>')

# api.add_resource(Train, '/train')
#
# api.add_resource(Hello, '/Test/<string:name>')

@app.route('/train', methods = ['POST'])
def execute_api():
    result = request.get_json()
    train = Train()
    data = result['data']
    print(data)
    train.post(data)
    return "trained"

if __name__ == '__main__':
    app.run(host='0.0.0.0')