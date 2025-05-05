# tests/integration/test_team_flow.py

from unittest.mock import MagicMock
from StatScraping import loginFunction, teamStatDisplay

def test_login_and_team_stat_display(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Login
    monkeypatch.setattr('builtins.input', lambda _: 'nbaFan99')
    mock_cursor.fetchone.return_value = ('nbaFan99',)

    user = loginFunction(mock_connection)
    assert user == 'nbaFan99'

    # Team stat display
    inputs = iter(['Los Angeles Lakers', 'no'])  # Team name, then exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    mock_cursor.fetchall.return_value = [
        (1, 'Los Angeles Lakers', '52-30', '30-11', '22-19')
    ]

    result = teamStatDisplay(mock_connection)
    assert result is True

    mock_cursor.execute.assert_called_with(
        'SELECT "Rk", "Team", "Overall", "Home", "Road" FROM "Team Stats" WHERE "Team" ILIKE %s',
        ('Los Angeles Lakers',)
    )
