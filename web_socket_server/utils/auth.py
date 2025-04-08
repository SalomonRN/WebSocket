from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
import jwt
from datetime import datetime, timedelta
from os import getenv
from hashlib import pbkdf2_hmac
import os
from utils.utils_mongo import get_user, create_user_in_db
SECRET = getenv("SECRET", "INSECURE_SECRET")


def create_user(username: str, password: str, email: str):
    password = _encode_password(password)
    return create_user_in_db(username, password, email)

def authenticate_user(auth: dict) -> bool|dict:
    user = get_user(auth.get('username', None))
    if not user:
        return False
    user.pop('_id')
    if not _check_pass(auth.get('password'), user.get('password')):
        return False
    
    print(user)
    user.pop('password')
    return user

def create_token(data: dict):
    return _encode_token(data)

def validate_token(token: str):
    status, verified = _decode_token(token)
    return status, verified

# FUNCIONES QUE SOLO SE LLAMA DESDE ESTE ARCHIVO

def _encode_password(password: str, salt = os.urandom(32), alghoritm = "sha256") -> str:
    hashed_password = pbkdf2_hmac(alghoritm, password.encode('utf-8'), salt, 100).hex()
    return f"{alghoritm}${salt.hex()}${hashed_password}"
   
def _check_pass(password: str, hash: str) -> bool:
    salt = hash.split('$')[1]
    return _encode_password(password, bytes.fromhex(salt)) == hash

def _exp_time(weeks= 0.0, days= 0.0, hours= 0.0, minutes= 0.0, seconds= 0.0) -> float:
    exp = datetime.now() + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return exp.timestamp()

def _encode_token(data: dict) -> str:
    data['exp'] = _exp_time(days=2)
    # data['exp'] = _exp_time(seconds=1)
    return jwt.encode(data, SECRET, algorithm="HS256")

def _decode_token(token: str) -> str | ExpiredSignatureError | InvalidSignatureError | DecodeError:
    try:
        return jwt.decode_complete(token, SECRET, algorithms=["HS256"], options={"verify_signature":True, "require": ["exp"]}), "pass"
    except ExpiredSignatureError as error:
        return None, error
    except InvalidSignatureError as error:
        return None, error
    except DecodeError as error:
        return None, "Token no valido"
    except Exception as error:
        print(type(error))
        return None, error

if __name__ == "__main__":
    from mongo import init_connection
    init_connection()
    create_user("salo3", "salo3", "salo2@salo.com")
