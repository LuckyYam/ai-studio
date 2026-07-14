from datetime import datetime, timedelta, timezone

import jwt

from core import JWT_ALGORITHM, JWT_EXPIRY_DAYS_DEFAULT, JWT_EXPIRY_DAYS_REMEMBERED


def create_auth_token(jwt_secret: str, user_id: str, remember_me: bool = False) -> str:
    days = JWT_EXPIRY_DAYS_REMEMBERED if remember_me else JWT_EXPIRY_DAYS_DEFAULT
    payload = {'sub': str(user_id), 'iat': datetime.now(timezone.utc), 'exp': datetime.now(timezone.utc) + timedelta(days=days)}
    return jwt.encode(payload, jwt_secret, algorithm=JWT_ALGORITHM)


def decode_auth_token(jwt_string: str, token: str):
    try:
        return jwt.decode(token, jwt_string, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as err:
        print('decode err:', err)
        return None
    except jwt.InvalidTokenError as err:
        print('decode err:', err)
        return None
