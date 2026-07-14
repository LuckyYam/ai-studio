import re
from datetime import datetime


def count_words(text: str) -> int:
    return len(text.split())


def highlight(text: str, keyword: str) -> str:
    if not keyword:
        return text
    return re.sub(re.escape(keyword), lambda x: f'<mark>{x.group()}</mark>', text, flags=re.IGNORECASE)


def get_timestamp() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def format_duration(start_time: datetime) -> str:
    diff_seconds = max(0, int((datetime.now() - start_time).total_seconds()))
    days, remainder = divmod(diff_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days >= 1:
        return f'{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}'
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def format_display_timestamp(raw: str) -> str:
    if not raw or raw == '—':
        return '—'
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(raw, fmt).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue
    return raw
