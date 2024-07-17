from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from app import mongo

def get_user_collection():
    return mongo.db.users

def get_user_by_username(username):
    user_collection = get_user_collection()
    user = user_collection.find_one({'userName': username})
    if user:
        print(f"Username found: {user['userName']}")
    else:
        print(f"Username '{username}' not found")
    return user

