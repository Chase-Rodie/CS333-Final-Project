# tests/integration/test_stat_flow.py

from unittest.mock import MagicMock
from StatScraping import loginFunction, regularStatDisplay

def test_login_and_regular_stat_display(monkeypatch):
    # ---- Setup: Mock connection and cursor ----
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # ---- Simulate user login ----
    monkeypatch.setattr('builtins.input', lambda _: 'lebron23')
    mock_cursor.fetchone.return_value = ('lebron23',)

    user = loginFunction(mock_connection)
    assert user == 'lebron23'
    mock_cursor.execute.assert_called_with('SELECT userid FROM "User Info" WHERE userid = %s', ('lebron23',))

    # ---- Simulate stat lookup ----
    inputs = iter(['LeBron James', 'no'])  # Player name, then exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Return mock player data
    mock_cursor.fetchall.return_value = [
        (1, 'LeBron James', 'LAL', 28.5, 7.2, 8.1)
    ]

    result = regularStatDisplay(mock_connection)
    assert result is True
    mock_cursor.execute.assert_called_with(
        'SELECT "RANK", "PLAYER", "TEAM", "PTS", "REB", "AST" FROM "Regular Season Stats 23-24" WHERE "PLAYER" ILIKE %s',
        ('LeBron James',)
    )
