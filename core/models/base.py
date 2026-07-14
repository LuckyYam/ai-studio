from datetime import datetime
from typing import TypedDict


class IDate(TypedDict):
    id: int
    created_at: datetime
    updated_at: datetime
