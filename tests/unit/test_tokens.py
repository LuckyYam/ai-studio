from datetime import datetime, timedelta, timezone
from typing import cast
import jwt as pyjwt
from auth.tokens import create_auth_token, decode_auth_token
from core import JWT_ALGORITHM, JWT_EXPIRY_DAYS_DEFAULT, JWT_EXPIRY_DAYS_REMEMBERED


def test_create_auth_token_roundtrips(jwt_secret: str):
    token = create_auth_token(jwt_secret, user_id='42')
    decoded = decode_auth_token(jwt_secret, token)
    assert decoded is not None
    assert decoded['sub'] == '42'


def test_create_auth_token_coerces_user_id_to_str(jwt_secret: str):
    token = create_auth_token(jwt_secret, user_id=cast(str, 42))
    decoded = decode_auth_token(jwt_secret, token)
    assert decoded is not None
    assert decoded['sub'] == '42'


def test_default_expiry_is_short(jwt_secret: str):
    token = create_auth_token(jwt_secret, user_id='1', remember_me=False)
    decoded = decode_auth_token(jwt_secret, token)
    assert decoded is not None
    exp = datetime.fromtimestamp(float(decoded['exp']), tz=timezone.utc)
    iat = datetime.fromtimestamp(float(decoded['iat']), tz=timezone.utc)
    delta = exp - iat
    assert timedelta(days=JWT_EXPIRY_DAYS_DEFAULT) - timedelta(seconds=5) <= delta <= timedelta(days=JWT_EXPIRY_DAYS_DEFAULT) + timedelta(seconds=5)


def test_remember_me_expiry_is_long(jwt_secret: str):
    token = create_auth_token(jwt_secret, user_id='1', remember_me=True)
    decoded = decode_auth_token(jwt_secret, token)
    assert decoded is not None
    exp = datetime.fromtimestamp(float(decoded['exp']), tz=timezone.utc)
    iat = datetime.fromtimestamp(float(decoded['iat']), tz=timezone.utc)
    delta = exp - iat
    assert timedelta(days=JWT_EXPIRY_DAYS_REMEMBERED) - timedelta(seconds=5) <= delta <= timedelta(days=JWT_EXPIRY_DAYS_REMEMBERED) + timedelta(seconds=5)


def test_decode_rejects_wrong_secret(jwt_secret: str):
    token = create_auth_token(jwt_secret, user_id='1')
    assert decode_auth_token('a-completely-different-secret', token) is None


def test_decode_rejects_expired_token(jwt_secret: str):
    payload = {
        'sub': '1',
        'iat': datetime.now(timezone.utc) - timedelta(days=2),
        'exp': datetime.now(timezone.utc) - timedelta(days=1),
    }
    expired_token = pyjwt.encode(payload, jwt_secret, algorithm=JWT_ALGORITHM)
    assert decode_auth_token(jwt_secret, expired_token) is None


def test_decode_rejects_garbage_token(jwt_secret: str):
    assert decode_auth_token(jwt_secret, 'not.a.jwt') is None


def test_decode_rejects_token_signed_with_different_algorithm(jwt_secret: str):
    payload = {'sub': '1', 'iat': datetime.now(timezone.utc), 'exp': datetime.now(timezone.utc) + timedelta(days=1)}
    token = pyjwt.encode(payload, jwt_secret, algorithm='HS512')
    assert decode_auth_token(jwt_secret, token) is None
