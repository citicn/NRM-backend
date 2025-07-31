from app import mongodb
from app.models.messages import Message

class MessageService:
    @staticmethod
    def send_message(sender_id, conversation_id, text):
        message = Message(sender_id=sender_id, conversation_id=conversation_id, text=text)
        result = mongodb.db.messages.insert_one(message.to_dict())
        message._id = result.inserted_id
        return message

    @staticmethod
    def get_messages_for_conversation(conversation_id):
        messages = mongodb.db.messages.find({"conversation_id": conversation_id}).sort("created_at", 1)
        return [Message.from_dict(msg) for msg in messages]
