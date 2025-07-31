from app import mongodb
from app.models.conversations import Conversation
from bson import ObjectId

class ConversationService:
    @staticmethod
    def create_conversation(data, cUserId):
        members = data.get("members", [])
        if cUserId not in members:
            members.append(cUserId)

        convType = data.get("conversation_type")
        gName = data.get("name") if convType == "group" else None

        conversation = Conversation(members=members, conversation_type=convType, name=gName)
        result = mongodb.db.conversations.insert_one(conversation.to_dict())
        conversation._id = result.inserted_id

        return conversation

    @staticmethod
    def get_conversation_by_id(conversation_id):
        try:
            convId = ObjectId(conversation_id)
        except Exception:
            return None
        data = mongodb.db.conversations.find_one({"_id": convId})
        return Conversation.from_dict(data) if data else None

    @staticmethod
    def find_conversation(user_id, other_user_id):
        members = [user_id, other_user_id]
        conv = mongodb.db.conversations.find_one({
            "members": {"$all": members, "$size": 2},
            "conversation_type": "private"
        })
        return Conversation.from_dict(conv) if conv else None

    @staticmethod
    def get_all_conversations_for_user(current_user_id):
        conversations = list(mongodb.db.conversations.find({
            "members": {"$in": [current_user_id]}
        }))

        results = []
        for conv in conversations:
            convId = str(conv.get("_id"))
            last_msg = mongodb.db.messages.find_one(
                {"conversation_id": convId},
                sort=[("created_at", -1)]
            )
            if last_msg:
                createdAt = last_msg.get("created_at")
                if createdAt and hasattr(createdAt, "isoformat"):
                    createdAt = createdAt.isoformat()
                elif createdAt is None:
                    createdAt = ""
                msg = {
                    "text": last_msg.get("text", ""),
                    "created_at": createdAt,
                    "sender_id": last_msg.get("sender_id", "")
                }
            else:
                msg = {
                    "text": "",
                    "created_at": "",
                    "sender_id": ""
                }

            membersData = []
            for memberId in conv.get("members", []):
                user = mongodb.db.users.find_one({"_id": ObjectId(memberId)})
                membersData.append({
                    "id": memberId,
                    "username": user["username"]
                })

            results.append({
                "id": convId,
                "members": membersData,
                "conversation_type": conv.get("conversation_type"),
                "name": conv.get("name"),
                "last_message": msg
            })

        results.sort(
            key=lambda x: x["last_message"]["created_at"] if x["last_message"] else "",
            reverse=True
        )

        return results
