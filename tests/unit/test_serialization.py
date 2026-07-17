import base64
from google.genai import types
from utils.serialization import (
    decode_history_from_storage,
    encode_history_for_storage,
    split_new_history_entries,
)


def _text_content(role: str, text: str) -> types.Content:
    return types.Content(role=role, parts=[types.Part(text=text)])


def _content_with_bytes(role: str, data: bytes, mime_type: str = 'image/png') -> types.Content:
    return types.Content(role=role, parts=[types.Part.from_bytes(data=data, mime_type=mime_type)])


def test_encode_history_produces_json_safe_dicts():
    history = [_text_content('user', 'zzz'), _text_content('model', 'zzzzz')]
    encoded = encode_history_for_storage(history)
    assert isinstance(encoded, list)
    assert encoded[0]['role'] == 'user'
    assert encoded[0]['parts'][0]['text'] == 'zzz'
    assert encoded[1]['role'] == 'model'


def test_encode_history_base64_encodes_raw_bytes():
    raw = b'\x89PNG\r\n\x1a\nnot-a-real-png'
    history = [_content_with_bytes('user', raw)]
    encoded = encode_history_for_storage(history)
    inline_data = encoded[0]['parts'][0]['inline_data']
    assert isinstance(inline_data['data'], dict)
    assert inline_data['data']['__b64__'] == base64.b64encode(raw).decode('ascii')


def test_decode_history_restores_original_bytes():
    raw = b'some-raw-attachment-bytes \x00\x01\x02'
    history = [_content_with_bytes('user', raw)]
    encoded = encode_history_for_storage(history)
    decoded = decode_history_from_storage(encoded)
    assert decoded[0]['parts'][0]['inline_data']['data'] == raw


def test_encode_decode_roundtrip_is_lossless_for_text():
    history = [_text_content('user', 'roundtrip me'), _text_content('model', 'okay')]
    roundtripped = decode_history_from_storage(encode_history_for_storage(history))
    assert roundtripped[0]['parts'][0]['text'] == 'roundtrip me'
    assert roundtripped[1]['parts'][0]['text'] == 'okay'


def test_split_new_history_entries_separates_user_from_model():
    entries = [
        {'role': 'user', 'parts': [{'text': 'prompt'}]},
        {'role': 'model', 'parts': [{'text': 'response part 1'}]},
        {'role': 'model', 'parts': [{'text': 'response part 2'}]},
    ]
    user_entry, model_entries = split_new_history_entries(entries)
    assert user_entry is not None
    assert user_entry['parts'][0]['text'] == 'prompt'
    assert len(model_entries) == 2
    assert all(e['role'] == 'model' for e in model_entries)


def test_split_new_history_entries_handles_no_user_entry():
    entries = [{'role': 'model', 'parts': [{'text': 'model turn'}]}]
    user_entry, model_entries = split_new_history_entries(entries)
    assert user_entry is None
    assert len(model_entries) == 1


def test_split_new_history_entries_only_takes_first_user_entry():
    entries = [
        {'role': 'user', 'parts': [{'text': 'first'}]},
        {'role': 'user', 'parts': [{'text': 'second'}]},
    ]
    user_entry, model_entries = split_new_history_entries(entries)
    assert user_entry is not None
    assert user_entry['parts'][0]['text'] == 'first'
    assert model_entries == []
