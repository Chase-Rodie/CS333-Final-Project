# tests/unit/test_login.py

from unittest.mock import MagicMock
from StatScraping import loginFunction

def test_login_success(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    monkeypatch.setattr('builtins.input', lambda _: 'user123')
    mock_cursor.fetchone.return_value = ('user123',)

    result = loginFunction(mock_connection)

    assert result == 'user123'
    mock_cursor.execute.assert_called_with(
        'SELECT userid FROM "User Info" WHERE userid = %s',
        ('user123',)
    )
    mock_cursor.close.assert_called_once()

def test_login_invalid_user(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    monkeypatch.setattr('builtins.input', lambda _: 'fakeuser')
    mock_cursor.fetchone.return_value = None

    result = loginFunction(mock_connection)

    assert result is None
    mock_cursor.execute.assert_called()
    mock_cursor.close.assert_called_once()
