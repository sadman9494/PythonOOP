import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://sadman:1234@cluster0.x8hev7r.mongodb.net/test')
