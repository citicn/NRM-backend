from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, create_refresh_token

authBp = Blueprint("auth", __name__)

@authBp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if UserService.get_user_by_username(data["username"]):
        return jsonify({"error": "Username vec postoji."}), 400

    user = UserService.create_user(
        username=data["username"],
        password=data["password"]
        )
    return jsonify(user.to_dict()), 201

@authBp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username=data.get("username")
    password=data.get("password")

    if not username or not password:
        return jsonify({"error":"Potrebni korisnicko ime i lozinka"}),400

    user= UserService.get_user_by_username(username)

    if not user or not UserService.verify_password(user, password):
        return jsonify({"error":"Neispravni kredencijali za logovanje"}), 401

    token = create_access_token(identity=str(user._id))
    refreshToken = create_refresh_token(identity=str(user._id))

    return jsonify({
        "access_token":token,
        "refresh_token":refreshToken,
        "user": user.to_dict()
    }),200

