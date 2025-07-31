import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY","falback-key")
    MONGO_URI=os.environ.get("MONGO_URI","mongodb://localhost:27017/nrm-secure-messaging")
    DEBUG = True
    JWT_SECRET_KEY = "12345678"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

