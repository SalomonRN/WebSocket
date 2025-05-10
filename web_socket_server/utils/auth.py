from typing import Union, Literal
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
import jwt
from datetime import datetime, timedelta
from os import getenv
from hashlib import pbkdf2_hmac
import os
from utils_mongo import get_user, create_user_in_db
SECRET = getenv("SECRET", "INSECURE_SECRET")

def create_user(username: str, password: str, email: str) -> Union[Literal[True], str]:
    """
    Create a user in the database with the given username, password and email.
    The password is hashed using PBKDF2 with SHA256 and a random salt.

    Args:
        username (str): Username of the user to be created.
        password (str): Password of the user to be created.
        email (str): Email of the user to be created.

    Returns:
        Union[Literal[True], str]: 
            - True if the user was created successfully.
            - A string with an error message if the creation failed.
            - False if the user was created successfully but an unexpected issue occurred.
    """
    password = _encode_password(password)
    res = create_user_in_db(username, password, email)
    
    if isinstance(res, dict):
        return res.get('error', "Error creating user")
    
    return True

def authenticate_user(auth: dict) -> Union[dict, Literal[False]]:
    """Authenticate a user with the given username and password.

    Args:
        auth (dict): Dictionary with the username and password of the user to be authenticated.

    Returns:
        User (dict): If the user was authenticated successfully, it will return a dict with the user data.
        bool (False): If the user was not authenticated, it will return False.
    """
    user = get_user(auth.get('username', None))
    if not user:
        return False
    user.pop('_id')
    if not _check_pass(auth.get('password'), user.get('password')):
        return False
    
    user.pop('password')
    return user

def create_token(data: dict):
    """Create a JWT with the given data.

    Args:
        data (dict): Dictionary with the data to be encoded in the JWT.

    Returns:
        _type_: _description_
    """
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
    """Calculate the expiration time of the token.

    Args:
        weeks (float, optional): Defaults to 0.0.
        days (float, optional): Defaults to 0.0.
        hours (float, optional): Defaults to 0.0.
        minutes (float, optional): Defaults to 0.0.
        seconds (float, optional): Defaults to 0.0.

    Returns:
        float: Expiration time of the token in seconds.
    """
    exp = datetime.now() + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return exp.timestamp()

def _encode_token(data: dict) -> str:
    data['exp'] = _exp_time(days=2)
    # data['exp'] = _exp_time(seconds=1)
    return jwt.encode(data, SECRET, algorithm="HS256")

def _decode_token(token: str) -> str | ExpiredSignatureError | InvalidSignatureError | DecodeError:
    """Decode a JWT with the given token.
    The token is verified with the secret key and the algorithm used to encode it.

    Args:
        token (str): Token to be decoded.

    Returns:
        str: If the token was decoded successfully, it will return the decoded data.
        ExpiredSignatureError | InvalidSignatureError | DecodeError:  Pass
    """
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
    a = create_user("wewqeqw", "salo3", "salo2@salo2.com")
    print(a)
