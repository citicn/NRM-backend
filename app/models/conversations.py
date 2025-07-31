from datetime import datetime
from bson import ObjectId

class Conversation:
    def __init__(self, members, conversation_type, name=None, created_at=None,_id=None):
        self._id = ObjectId(_id)
        self.members = members
        self.conversation_type = conversation_type
        self.name = name
        self.created_at = created_at or datetime.now()

    @staticmethod
    def from_dict(data):
        return Conversation(
            members=data.get("members", []),
            conversation_type=data.get("conversation_type"),
            name=data.get("name"),
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )

    def to_dict(self):
        return {
            "id": str(self._id),
            "members": self.members,
            "conversation_type": self.conversation_type,
            "name": self.name,
            "created_at": self.created_at.isoformat()
        }
