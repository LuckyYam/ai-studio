from typing import TypedDict


class IToken(TypedDict):
    sub: str
    iat: float
    exp: float
