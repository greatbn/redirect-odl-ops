from flask import Flask, g
from flask_restful import Api

from resources.handlers import RootResource, HandleAttackResource, ManageAttackResource
from mongodb import MongoDBWrapper

def create_app():

    app = Flask('dvnh-api')
    api = Api(app)

    api.add_resource(RootResource, "/")
    api.add_resource(HandleAttackResource, "/handle_attack")
    api.add_resource(ManageAttackResource, "/attack/attacker/<string:attacker_ip>/victim/<string:victim_ip>")


    db = MongoDBWrapper()

    app.db = db
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=9000)