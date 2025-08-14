from pymongo.collation import Collation
from pymongo import ASCENDING
from app import mongodb
from app.models.user import User
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
class UserService:

    @staticmethod
    def create_user(username, password):
        password_hash = generate_password_hash(password)
        user = User(username, password_hash)
        result = mongodb.db.users.insert_one(user.to_dict())
        user._id = result.inserted_id
        return user

    @staticmethod
    def get_user_by_username(username):
        user = mongodb.db.users.find_one({"username": username})
        return User.from_dict(user) if user else None

    @staticmethod
    def get_user_by_id(user_id):
        try:
            userId = ObjectId(user_id)
        except Exception:
            return None
        user = mongodb.db.users.find_one({"_id": userId})
        return User.from_dict(user).user_data() if user else None

    @staticmethod
    def verify_password(user: User, password):
        return check_password_hash(user.password_hash, password)


    @staticmethod
    def update_user(user_id, updates: dict):
        fields = ["bio", "profile_picture"]
        updates = {k: v for k, v in updates.items() if k in fields}

        result = mongodb.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updates}
        )
        return result.modified_count > 0

    @staticmethod
    def get_all_users():
        coll= Collation(locale='en',strength=2)
        users = mongodb.db.users.find().sort("username", ASCENDING).collation(coll)
        return [User.from_dict(doc).user_data() for doc in users]

