from unittest.mock import MagicMock
import psycopg2
from StatScraping import signupFunction
from StatScraping import loginFunction


def test_signup_success_new_user(monkeypatch):
    # Mock cursor and connection
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Simulate user input
    monkeypatch.setattr('builtins.input', lambda _: 'newuser')

    # Simulate no existing user
    mock_cursor.fetchone.return_value = None

    result = signupFunction(mock_connection)

    assert result == 'newuser'
    mock_cursor.execute.assert_any_call('INSERT INTO "User Info" (userid) VALUES (%s)', ('newuser',))
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_signup_existing_user(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    monkeypatch.setattr('builtins.input', lambda _: 'existinguser')

    # Simulate user already exists
    mock_cursor.fetchone.return_value = ('existinguser',)

    result = signupFunction(mock_connection)

    assert result is False
    mock_cursor.execute.assert_called_with('SELECT userid FROM "User Info" WHERE userid = %s', ('existinguser',))
    mock_connection.commit.assert_not_called()
    mock_cursor.close.assert_called_once()

def test_signup_db_exception(monkeypatch):
    mock_connection = MagicMock()
    mock_connection.cursor.side_effect = psycopg2.Error("DB error")  # 👈 FIXED

    monkeypatch.setattr('builtins.input', lambda _: 'userfail')

    result = signupFunction(mock_connection)
    assert result is None

def test_login_invalid_user(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    monkeypatch.setattr("builtins.input", lambda _: "notarealuser")
    mock_cursor.fetchone.return_value = None

    result = loginFunction(mock_connection)

    assert result is None
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
