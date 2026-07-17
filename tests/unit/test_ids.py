import re
from utils.ids import base36, generate_conversation_id


def test_base36_zero():
    assert base36(0) == '0'


def test_base36_known_values():
    assert base36(35) == 'z'
    assert base36(36) == '10'
    assert base36(1295) == 'zz'


def test_base36_is_monotonically_non_decreasing_in_length():
    assert len(base36(36**3)) >= len(base36(36**2))


def test_generate_conversation_id_format():
    conv_id = generate_conversation_id()
    time_part, _, uuid_part = conv_id.partition('-')
    assert re.fullmatch(r'[0-9a-z]+', time_part)
    assert re.fullmatch(r'[0-9a-f]{32}', uuid_part)


def test_generate_conversation_id_is_unique_across_calls():
    ids = {generate_conversation_id() for _ in range(1000)}
    assert len(ids) == 1000
