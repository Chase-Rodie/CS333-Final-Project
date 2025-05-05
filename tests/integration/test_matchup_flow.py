# tests/integration/test_matchup_flow.py

from unittest.mock import MagicMock
from StatScraping import loginFunction, matchupStatDisplay

def test_login_and_matchup_stat_display(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Login
    monkeypatch.setattr('builtins.input', lambda _: 'courtVision')
    mock_cursor.fetchone.return_value = ('courtVision',)

    user = loginFunction(mock_connection)
    assert user == 'courtVision'

    # Matchup stat display
    inputs = iter(['Wed Apr 24 2024', 'no'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    mock_cursor.fetchall.return_value = [
        ('Wed Apr 24 2024', 'BOS', 'MIA', 'TD Garden', 'BOS')
    ]

    result = matchupStatDisplay(mock_connection)
    assert result is True

    mock_cursor.execute.assert_called_with(
        'SELECT "Date", "Visitor/Neutral", "Home/Neutral", "Arena", "Winner" FROM "Matchup Schedule" WHERE "Date" ILIKE %s',
        ('Wed Apr 24 2024',)
    )
