import os, jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
hasher = CryptContext(schemes=['bcrypt'])
secret = str(os.getenv("APP_SECRET_STRING"))

def encode_password(password):
    return hasher.hash(password)

def verify_password(password, encoded_password):
    return hasher.verify(password, encoded_password)

def encode_token(username):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, hours=1),
        'iat': datetime.utcnow(),
        'scope': 'access_token',
        'sub': username
    }
    return jwt.encode(
        payload,
        secret,
        algorithm='HS256'
    )

def decode_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        if (payload['scope'] == 'access_token'):
            return {payload['sub']}
        raise HTTPException(status_code=401, detail='Scope for the token is invalid')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')

def encode_refresh_token(username):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, hours=10),
        'iat': datetime.utcnow(),
        'scope': 'refresh_token',
        'sub': username
    }
    return jwt.encode(
        payload,
        secret,
        algorithm='HS256'
    )

def refr_token(refr_token):
    try:
        payload = jwt.decode(refr_token, secret, algorithms=['HS256'])
        if (payload['scope'] == 'refresh_token'):
            username = payload['sub']
            new_token = encode_token(username)
            return new_token
        raise HTTPException(status_code=401, detail='Invalid scope for token')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid refresh token')