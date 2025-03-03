from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
import json
import jwt
from datetime import datetime, timedelta
from os import getenv
from hashlib import pbkdf2_hmac
import os
from utils_mongo import get_user, create_user_in_db
import time
from base64 import b64decode, b64encode, urlsafe_b64encode
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
    # data['exp'] = _exp_time(days=2)
    data['exp'] = _exp_time(seconds=1)
    return jwt.encode(data, SECRET, algorithm="HS256")

def _decode_token(token: str) -> str | ExpiredSignatureError | InvalidSignatureError | DecodeError:
    try:
        return jwt.decode_complete(token, SECRET, algorithms=["HS256"], options={"verify_signature":True, "require": ["exp"]})
    except ExpiredSignatureError as error:
        return error, "pass"
    except InvalidSignatureError as error:
        return None, error
    except DecodeError as error:
        return None, "Token no valido"
    except Exception as error:
        print(type(error))
        return None, error

if __name__ == "__main__":
    pass
    token = _encode_token({"username": "salo", "email": "salo@salo.cm"})
    time.sleep(2)
    print(validate_token(token))
    # header, payload,signature = token.split('.')
    # payload = b64decode(payload+"==").decode()
    # payload = json.loads(payload)
    # payload['admin'] = "True"
    # payload = json.dumps(payload).encode()
    # print(payload)
    # token = f"{header}.{urlsafe_b64encode(payload).decode().replace("==", '')}.{signature}"
    # print(token)
    # print(_decode_token(token))
    

    # time.sleep(4)
    # decoded_token = _decode_token(token)
    # print(decoded_token)
    # from mongo import init_connection
    # init_connection()
    # create_user("salo2", "salopass", "email@email.com")
    # user = authenticate_user({"username": "salo", "password": "salo"})
    
    
    # print(authenticate_user({"username": "salo", "password": "salo"}))

    # print(base64.b64encode("salo"))
    # encoded = base64.b64encode('salomon'.encode())
    # print(encoded)

    # decoded = base64.b64decode("MjIyMDIyMTA0MQ==")
    # print(decoded.decode())

    # char = chr(65)
    # print(char)
    # encoded = char.encode("utf-8")
    # print(encoded)
    # decoded = encoded.decode()  # Lo decodificamos de vuelta
    # print(decoded)