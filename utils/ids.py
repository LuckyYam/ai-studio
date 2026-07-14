import uuid
from datetime import datetime


def generate_conversation_id() -> str:
    id_part = uuid.uuid4().hex
    time_part = base36(int(datetime.now().timestamp()))
    return f'{time_part}-{id_part}'


def base36(num: int) -> str:
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''
    while num:
        num, rem = divmod(num, 36)
        result = chars[rem] + result
    return result or '0'
