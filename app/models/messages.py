from datetime import datetime
from bson import ObjectId

class Message:
    def __init__(self, sender_id, conversation_id, text, created_at=None,_id=None):
        self._id = ObjectId(_id)
        self.attachment = None
        self.sender_id = sender_id
        self.conversation_id = conversation_id
        self.text = text
        self.created_at = datetime.now() or created_at

    def to_dict(self):
        return {
            "sender_id": self.sender_id,
            "conversation_id": self.conversation_id,
            "text": self.text,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        return Message(
            sender_id=data.get("sender_id"),
            conversation_id=data.get("conversation_id"),
            text=data.get("text"),
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )
