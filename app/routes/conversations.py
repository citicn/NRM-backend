from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.conversations_service import ConversationService

conversationsBp = Blueprint("conversations", __name__)

@conversationsBp.route("/conversations/create", methods=["POST"])
@jwt_required()
def create_conv():
    data = request.get_json()
    cUserId = get_jwt_identity()
    conversation = ConversationService.create_conversation(data, cUserId)
    return jsonify(conversation.to_dict()), 201

@conversationsBp.route("/conversations/<conversation_id>", methods=["GET"])
@jwt_required()
def get_conv(conversation_id):
    conversation = ConversationService.get_conversation_by_id(conversation_id)
    if not conversation:
        return jsonify({"error": "Konverzacija nije pronadjena"}), 404
    return jsonify(conversation.to_dict()), 200

@conversationsBp.route("/conversations/find", methods=["POST"])
@jwt_required()
def find_conv():
    data = request.get_json()
    cUserId = get_jwt_identity()
    oUserId = data.get("other_user_id")
    if not oUserId:
        return jsonify({"error": "Fali user id"}), 400
    conversation = ConversationService.find_conversation(cUserId, oUserId)
    if conversation:
        return jsonify(conversation.to_dict()), 200
    else:
        return jsonify({"error": "Nije pronadjena konverzacija"}), 404

@conversationsBp.route("/conversations", methods=["GET"])
@jwt_required()
def get_all_conv():
    cUserId = get_jwt_identity()
    results = ConversationService.get_all_conversations_for_user(cUserId)
    return jsonify(results), 200
