from flask_restful import Resource
import json
# from models.models import Model

todos = {}
class Hello(Resource):
    def get(self,name):
        print(name)
        
        return {'name': name} 