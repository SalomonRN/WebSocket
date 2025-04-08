from utils import mongo

def create_user_in_db(username: str, password: str, email: str):
    
    querry = {
        "username": username,
        "password": password,
        "email": email
    }
    return mongo.create_user(querry)

def get_user(username: str) -> dict:
   return mongo.get_user(username)
