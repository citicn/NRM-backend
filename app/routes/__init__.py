from .auth import authBp
from .users import usersBp
from .messages import messagesBp
from .conversations import conversationsBp
from .uploads import uploadsBp

blueprints = [
    authBp,
    usersBp,
    messagesBp,
    conversationsBp,
    uploadsBp
]

