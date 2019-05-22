from flask import request, current_app as app

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
        print(body_json_data)
        data, errors = HandleAttackSchema().load(body_json_data)
        if errors:
            return errors, 400

        # Check if exist
        flow = app.db.find_flow({
            'attacker_ip': data['attacker_ip'],
            'victim_ip': data['victim_ip']
        })
        if flow:
            mess = {"messsage": "Attacker and victim is exist"}
            app.logger.info(mess)
            return mess, 400
        # If not send to worker

        from worker.handler import add_flow_handler
        add_flow_handler.delay(data)
        mess = {"message": "Accepted request, We will handle it now"}
        return mess, 201
        

# class ManageAttackResource(Resource):

#     def get(self):

