import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def validate_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))
