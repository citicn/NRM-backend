from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.message_service import MessageService

messagesBp = Blueprint("messages", __name__)

@messagesBp.route("/messages/send", methods=["POST"])
@jwt_required()
def send_msg():
    data = request.get_json()
    cUserId = get_jwt_identity()
    convId = data.get("conversation_id")
    msgText = data.get("text")

    if not convId or not msgText:
        return jsonify({"error": "Fali id korisnika ili text poruke"}), 400

    message = MessageService.send_message(
        sender_id=cUserId,
        conversation_id=convId,
        text=msgText
    )
    return jsonify(message.to_dict()), 201

@messagesBp.route("/messages/<conversation_id>", methods=["GET"])
@jwt_required()
def get_msg(conversation_id):
    messages = MessageService.get_messages_for_conversation(conversation_id)
    return jsonify([message.to_dict() for message in messages]), 200


