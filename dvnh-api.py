from flask import Flask
from flask_restful import Api

from resources.handlers import RootResource, HandleAttackResource

def create_app():

    app = Flask('dvnh-api')
    api = Api(app)

    api.add_resource(RootResource, "/")
    api.add_resource(HandleAttackResource, "/handle_attack")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)