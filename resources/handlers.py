from flask import request

from flask_restful import Resource
from schema.handle_attack import HandleAttackSchema


class RootResource(Resource):

    def get(self):
        info = {
            "project_name": "Dynamic Virtual Network Honeypot",
            "author": "Sa Pham Dang",
            "email": "saphi070@gmail.com",
            "address": "SNSLab - System and Network Security Laboratory"
        }
        return info


class HandleAttackResource(Resource):
    def post(self):
        body_json_data = request.get_json()
        data, errors = HandleAttackSchema.load(body_json_data)
        if errors:
            return errors, 400


        # Check if exist 

        # If not send to worker
        