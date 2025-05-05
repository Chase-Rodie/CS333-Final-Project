# tests/integration/test_user_flow.py

from unittest.mock import MagicMock
from StatScraping import signupFunction, loginFunction, addFeedback

def test_signup_login_add_feedback(monkeypatch):
    # Mock database connection and cursor
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # -------- SIGNUP --------
    monkeypatch.setattr('builtins.input', lambda _: 'testuser1')
    mock_cursor.fetchone.return_value = None  

    user_id = signupFunction(mock_connection)
    assert user_id == 'testuser1'
    mock_cursor.execute.assert_any_call('INSERT INTO "User Info" (userid) VALUES (%s)', ('testuser1',))

    # -------- LOGIN --------
    monkeypatch.setattr('builtins.input', lambda _: 'testuser1')
    mock_cursor.fetchone.return_value = ('testuser1',)

    logged_in_user = loginFunction(mock_connection)
    assert logged_in_user == 'testuser1'
    mock_cursor.execute.assert_called_with('SELECT userid FROM "User Info" WHERE userid = %s', ('testuser1',))

    # -------- ADD FEEDBACK --------
    monkeypatch.setattr('builtins.input', lambda _: 'I love the stat interface!')
    result = addFeedback(mock_connection, 'testuser1')
    assert result is True
    mock_cursor.execute.assert_any_call(
        'INSERT INTO "User Info" (userid, feedback) VALUES (%s, %s)',
        ('testuser1', 'I love the stat interface!')
    )
    mock_connection.commit.assert_called()
