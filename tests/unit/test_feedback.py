# tests/unit/test_feedback.py

from unittest.mock import MagicMock
from StatScraping import addFeedback
import psycopg2

def test_add_feedback_success(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    monkeypatch.setattr('builtins.input', lambda _: 'Add WNBA stats please!')

    result = addFeedback(mock_connection, 'user123')

    assert result is True
    mock_cursor.execute.assert_called_with(
        'INSERT INTO "User Info" (userid, feedback) VALUES (%s, %s)',
        ('user123', 'Add WNBA stats please!')
    )
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_add_feedback_failure(monkeypatch):
    mock_connection = MagicMock()
    mock_connection.cursor.side_effect = psycopg2.Error("DB error")  

    monkeypatch.setattr('builtins.input', lambda _: 'Bad input')

    result = addFeedback(mock_connection, 'user123')
    assert result is False
