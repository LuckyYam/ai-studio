from unittest.mock import MagicMock
import pytest


@pytest.fixture
def jwt_secret() -> str:
    return 'jwt_secret_blah_blah_blah'


@pytest.fixture
def mock_db_pool(monkeypatch: pytest.MonkeyPatch):
    from mysql.connector import pooling

    mock_pool_instance = MagicMock()
    mock_conn = MagicMock()
    mock_pool_instance.get_connection.return_value = mock_conn
    mock_conn.ping.return_value = None
    monkeypatch.setattr(pooling, 'MySQLConnectionPool', MagicMock(return_value=mock_pool_instance))
    return mock_pool_instance


@pytest.fixture
def mock_genai_client(monkeypatch: pytest.MonkeyPatch):
    client = MagicMock()
    return client
