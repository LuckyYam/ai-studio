from unittest.mock import MagicMock
import pytest
from google.genai import types
from google.genai.errors import APIError
from core.chatbot import get_chat, get_chat_title
from core.config import GEMINI_2_MODELS


def test_get_chat_calls_client_with_expected_model(mock_genai_client: MagicMock):
    get_chat(mock_genai_client, model='gemini-3.1-flash-lite')
    mock_genai_client.chats.create.assert_called_once()
    _, kwargs = mock_genai_client.chats.create.call_args
    assert kwargs['model'] == 'gemini-3.1-flash-lite'


def test_get_chat_returns_the_created_chat(mock_genai_client: MagicMock):
    sentinel_chat = MagicMock()
    mock_genai_client.chats.create.return_value = sentinel_chat
    result = get_chat(mock_genai_client)
    assert result is sentinel_chat


def test_get_chat_uses_structured_output_when_web_search_disabled(mock_genai_client: MagicMock):
    get_chat(mock_genai_client, model='gemini-3.1-flash-lite', web_search=False)
    _, kwargs = mock_genai_client.chats.create.call_args
    config = kwargs['config']
    assert config.response_mime_type == 'application/json'
    assert config.system_instruction is not None


def test_get_chat_disables_structured_output_when_web_search_enabled_on_gemini2(mock_genai_client: MagicMock):
    gemini2_model = GEMINI_2_MODELS[0]
    get_chat(mock_genai_client, model=gemini2_model, web_search=True)
    _, kwargs = mock_genai_client.chats.create.call_args
    config = kwargs['config']
    assert config.response_mime_type is None
    assert config.system_instruction is None


def test_get_chat_web_search_flag_is_ignored_for_non_gemini2_models(mock_genai_client: MagicMock):
    get_chat(mock_genai_client, model='gemini-3.1-flash-lite', web_search=True)
    _, kwargs = mock_genai_client.chats.create.call_args
    config = kwargs['config']
    assert config.response_mime_type == 'application/json'


def test_get_chat_passes_through_generation_params(mock_genai_client: MagicMock):
    get_chat(mock_genai_client, temperature=0.7, maximum_output_tokens=512, top_k=40, top_p=0.8)
    _, kwargs = mock_genai_client.chats.create.call_args
    config = kwargs['config']
    assert config.temperature == 0.7
    assert config.max_output_tokens == 512
    assert config.top_k == 40
    assert config.top_p == 0.8


def test_get_chat_wraps_api_error_as_runtime_error(mock_genai_client: MagicMock):
    mock_genai_client.chats.create.side_effect = APIError(503, {'message': 'model overloaded'})
    with pytest.raises(RuntimeError, match='model overloaded'):
        get_chat(mock_genai_client)


def test_get_chat_wraps_unexpected_error_as_runtime_error(mock_genai_client: MagicMock):
    mock_genai_client.chats.create.side_effect = ValueError('boom')
    with pytest.raises(RuntimeError, match='Unexpected error occurred'):
        get_chat(mock_genai_client)


def test_get_chat_title_returns_stripped_text(mock_genai_client: MagicMock):
    mock_response = MagicMock()
    mock_response.text = '  A Chat About Cats  '
    mock_genai_client.models.generate_content.return_value = mock_response
    title = get_chat_title(mock_genai_client, ['tell me about cats'])
    assert title == 'A Chat About Cats'


def test_get_chat_title_raises_when_no_parts_given(mock_genai_client: MagicMock):
    with pytest.raises(RuntimeError, match='Nothing to generate a title from'):
        get_chat_title(mock_genai_client, [])
    mock_genai_client.models.generate_content.assert_not_called()


def test_get_chat_title_raises_when_response_has_no_text(mock_genai_client: MagicMock):
    mock_response = MagicMock()
    mock_response.text = None
    mock_genai_client.models.generate_content.return_value = mock_response
    with pytest.raises(RuntimeError, match="Couldn't generate the title"):
        get_chat_title(mock_genai_client, ['hi'])


def test_get_chat_title_enables_url_context_tool_when_url_present(mock_genai_client: MagicMock):
    mock_response = MagicMock()
    mock_response.text = 'Some Title'
    mock_genai_client.models.generate_content.return_value = mock_response
    get_chat_title(mock_genai_client, ['check out https://example.com please'])
    _, kwargs = mock_genai_client.models.generate_content.call_args
    config = kwargs['config']
    assert config.tools is not None
    assert config.max_output_tokens == 200


def test_get_chat_title_skips_url_context_tool_when_no_url(mock_genai_client: MagicMock):
    mock_response = MagicMock()
    mock_response.text = 'Some Title'
    mock_genai_client.models.generate_content.return_value = mock_response
    get_chat_title(mock_genai_client, ['just plain text, no links'])
    _, kwargs = mock_genai_client.models.generate_content.call_args
    config = kwargs['config']
    assert config.tools is None
    assert config.max_output_tokens == 20


def test_get_chat_title_accepts_mixed_str_and_part_input(mock_genai_client: MagicMock):
    mock_response = MagicMock()
    mock_response.text = 'Mixed Title'
    mock_genai_client.models.generate_content.return_value = mock_response
    image_part = types.Part.from_bytes(data=b'fake-bytes', mime_type='image/png')
    title = get_chat_title(mock_genai_client, ['describe this image', image_part])
    assert title == 'Mixed Title'
    mock_genai_client.models.generate_content.assert_called_once()


def test_get_chat_title_wraps_api_error_as_runtime_error(mock_genai_client: MagicMock):
    mock_genai_client.models.generate_content.side_effect = APIError(429, {'message': 'rate limited'})
    with pytest.raises(RuntimeError, match='rate limited'):
        get_chat_title(mock_genai_client, ['hello'])
