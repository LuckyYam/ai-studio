from datetime import datetime, timedelta
from utils.text import (
    count_words,
    format_display_timestamp,
    format_duration,
    get_timestamp,
    highlight,
)


def test_count_words_basic():
    assert count_words('cheese pizza') == 2


def test_count_words_collapses_extra_whitespace():
    assert count_words('  weeee   bruhhhh  \n foo') == 3


def test_count_words_empty_string():
    assert count_words('') == 0


def test_count_words_whitespace_only():
    assert count_words('   \n\t  ') == 0


def test_highlight_wraps_match_in_mark_tag():
    result = highlight('random string', 'string')
    assert result == 'random <mark>string</mark>'


def test_highlight_is_case_insensitive():
    result = highlight('i HaTe X', 'hate')
    assert result == 'i <mark>HaTe</mark> X'


def test_highlight_wraps_all_occurrences():
    result = highlight('blah blah blah', 'blah')
    assert result == '<mark>blah</mark> <mark>blah</mark> <mark>blah</mark>'


def test_highlight_returns_original_text_when_keyword_empty():
    assert highlight('no-keyword-here', '') == 'no-keyword-here'


def test_highlight_escapes_regex_special_characters_in_keyword():
    result = highlight('nisekoi season 3', 'season')
    assert result == 'nisekoi <mark>season</mark> 3'


def test_get_timestamp_format():
    ts = get_timestamp()
    parsed = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
    assert isinstance(parsed, datetime)


def test_format_duration_under_a_day():
    start = datetime.now() - timedelta(hours=1, minutes=2, seconds=3)
    result = format_duration(start)
    hours, minutes, seconds = result.split(':')
    assert hours == '01'
    assert minutes == '02'
    assert seconds.isdigit() and len(seconds) == 2


def test_format_duration_over_a_day_includes_days_segment():
    start = datetime.now() - timedelta(days=2, hours=3)
    result = format_duration(start)
    parts = result.split(':')
    assert len(parts) == 4
    assert parts[0] == '02'


def test_format_duration_future_start_time_clamps_to_zero():
    start = datetime.now() + timedelta(hours=1)
    result = format_duration(start)
    assert result == '00:00:00'


def test_format_display_timestamp_passthrough_for_em_dash():
    assert format_display_timestamp('—') == '—'


def test_format_display_timestamp_passthrough_for_empty_string():
    assert format_display_timestamp('') == '—'


def test_format_display_timestamp_normalizes_iso_format():
    result = format_display_timestamp('2026-07-17T09:30:00')
    assert result == '2026-07-17 09:30:00'


def test_format_display_timestamp_normalizes_iso_format_with_microseconds():
    result = format_display_timestamp('2026-07-17T09:30:00.123456')
    assert result == '2026-07-17 09:30:00'


def test_format_display_timestamp_already_normalized_is_unchanged():
    result = format_display_timestamp('2026-07-17 09:30:00')
    assert result == '2026-07-17 09:30:00'


def test_format_display_timestamp_unparseable_input_returned_as_is():
    result = format_display_timestamp('not-a-real-timestamp')
    assert result == 'not-a-real-timestamp'
