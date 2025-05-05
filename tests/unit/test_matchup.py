# tests/unit/test_matchup.py

from unittest.mock import MagicMock
from StatScraping import matchupStatDisplay

from StatScraping import teamStatDisplay

def test_team_stat_display_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    inputs = iter(["Boston Celtics", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = [
        (1, "Boston Celtics", "62-20", "37-4", "25-16")
    ]

    result = teamStatDisplay(mock_connection)
    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_team_stat_display_not_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    inputs = iter(["Bad Team"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = []

    result = teamStatDisplay(mock_connection)
    assert result is False
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
