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
        admin = cUserId if convType == "group" else None

        conversation = Conversation(members=members, conversation_type=convType, name=gName, admin=admin)
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
    def get_all_conversations_for_user(cUserId):
        conversations = list(mongodb.db.conversations.find({
            "members": {"$in": [cUserId]}
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
                "last_message": msg,
                "admin": conv.get("admin")
            })

        results.sort(
            key=lambda x: x["last_message"]["created_at"] if x["last_message"] else "",
            reverse=True
        )

        return results

    @staticmethod
    def add_member(convId, membersId, cUserId):
        conv = mongodb.db.conversations.find_one({"_id": ObjectId(convId)})
        if not conv:
            return {"error": "Konverzacija ne postoji"}, 404

        if conv.get("admin") != cUserId:
            return {"error": "Samo admin moze dodavati nove clanove"}, 403

        updatedMembers = set(conv["members"])
        updatedMembers.update(membersId)

        mongodb.db.conversations.update_one(
                {"_id": ObjectId(convId)},
                {"$set": {"members": list(updatedMembers)}}
            )

        updatedConv = mongodb.db.conversations.find_one({"_id": ObjectId(convId)})
        return Conversation.from_dict(updatedConv).to_dict(), 200

    @staticmethod
    def remove_member(convId, membersId, cUserId):
        conv = mongodb.db.conversations.find_one({"_id": ObjectId(convId)})
        if not conv:
            return {"error": "Konverzacija ne postoji"}, 404

        if conv.get("admin") != cUserId:
            return {"error": "Samo admin moze uklanjati clanove"}, 403

        if membersId == conv.get("admin"):
            return {"error": "Ne mozes obrisati admina"}, 400

        updatedMembers=[m for m in conv["members"] if m not in membersId]

        mongodb.db.conversations.update_one(
                {"_id": ObjectId(convId)},
                {"$set": {"members": updatedMembers}}
            )

        updatedConv = mongodb.db.conversations.find_one({"_id": ObjectId(convId)})
        return Conversation.from_dict(updatedConv).to_dict(), 200

    @staticmethod
    def delete_group(convId, cUserId):
        conversation = mongodb.db.conversations.find_one({"_id": ObjectId(convId)})
        if not conversation:
            return {"error": "Konverzacija ne postoji"}, 404

        if conversation.get("admin") != cUserId:
            return {"error": "Samo admin moze obrisati grupu"}, 403

        mongodb.db.messages.delete_many({"conversation_id": str(convId)})
        mongodb.db.conversations.delete_one({"_id": ObjectId(convId)})

        return {"message": "Grupa uspesno obrisana"}, 200




