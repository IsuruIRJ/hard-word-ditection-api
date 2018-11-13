from flask import Flask
from flask_restful import Api
from resources.Hello import Hello
from models.models import Model
from models.train import Train
from models.predict import Predict
from flask import request
from flask import jsonify
import json

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

api.add_resource(Model, '/test_app/<string:number>')

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

@app.route('/predict', methods = ['POST'])
def execute_api2():
    result = request.get_json()
    predict = Predict()
    data = result['data']
    feed = result['feed']
    output = predict.post(data,feed)
    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0')