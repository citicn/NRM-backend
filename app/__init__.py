from datetime import datetime
from bson import ObjectId
from flask import Flask
from .config import Config
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity

mongodb = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mongodb.init_app(app)
    jwt.init_app(app)


    @app.before_request
    def update_last_seen():
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                mongodb.db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"last_seen": datetime.now()}}
                )
        except Exception:
            pass

    from .routes import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix="/")

    return app
