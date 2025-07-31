from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.file_util import saveImg

usersBp = Blueprint("users", __name__)

@usersBp.route("/users", methods=["GET"])
@jwt_required()
def get_all_usr():
    users = UserService.get_all_users()
    return jsonify([user for user in users]), 200

@usersBp.route("/users/<user_id>", methods=["GET"])
@jwt_required()
def get_usr_by_id(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Korisnik nije pronadjen"}), 404
    return jsonify(user), 200

@usersBp.route("/users/<user_id>", methods=["PUT"])
@jwt_required()
def update_usr(user_id):
    cUser = get_jwt_identity()
    if str(cUser) != str(user_id):
        return jsonify({"error": "Neautorizovano"}), 403

    updates = request.form.to_dict()
    profileImg = request.files.get('profile_image')
    if profileImg:
        filename = saveImg(profileImg)
        if filename:
            updates['profile_picture'] = filename

    updatedUser = UserService.update_user(user_id, updates)
    if not updatedUser:
        return jsonify({"error": "Azuriranje neuspesno"}), 400
    return jsonify({"message": "Korisnik uspesno azuriran"}), 200




