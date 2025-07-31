from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self,username, password_hash, profile_picture=None, created_at=None, bio=None, last_seen=None, _id=None):
        self._id = ObjectId(_id)
        self.username=username
        self.password_hash=password_hash
        self.created_at= created_at or datetime.now()
        self.profile_picture=profile_picture
        self.bio=bio
        self.last_seen=last_seen


    @staticmethod
    def from_dict(data):

        return User(
            username=data.get("username"),
            password_hash=data.get("password_hash"),
            profile_picture=data.get("profile_picture"),
            created_at=data.get("created_at"),
            bio=data.get("bio"),
            _id=data.get("_id"),
            last_seen=data.get("last_seen")
        )

    def to_dict(self):
        return {
            "id": str(self._id),
            "username": self.username,
            "password_hash": self.password_hash,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at,
            "bio":self.bio,
            "last_seen":self.last_seen
        }

    def user_data(self):
        return {
            "id": str(self._id),
            "username": self.username,
            "profile_picture": self.profile_picture,
            "bio":self.bio,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None
        }
