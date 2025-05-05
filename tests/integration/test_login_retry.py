# tests/integration/test_login_retry.py

from unittest.mock import MagicMock
from StatScraping import loginFunction

def test_login_retry(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # First input = bad user, Second input = valid user
    inputs = iter(['wronguser', 'gooduser'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Simulate first fetch returns None, second returns valid user
    mock_cursor.fetchone.side_effect = [None, ('gooduser',)]

    result1 = loginFunction(mock_connection)
    assert result1 is None 

    result2 = loginFunction(mock_connection)
    assert result2 == 'gooduser'
