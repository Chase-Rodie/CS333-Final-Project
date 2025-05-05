# tests/unit/test_team.py

from unittest.mock import MagicMock
from StatScraping import teamStatDisplay

def test_team_stat_display_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Simulate user entering a valid team and then choosing 'no'
    inputs = iter(["Boston Celtics", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Simulate a matching team found
    mock_cursor.fetchall.return_value = [
        (1, "Boston Celtics", "60-22", "32-9", "28-13")
    ]

    result = teamStatDisplay(mock_connection)

    assert result is True
    mock_cursor.execute.assert_called_with(
        'SELECT "Rk", "Team", "Overall", "Home", "Road" FROM "Team Stats" WHERE "Team" ILIKE %s',
        ("Boston Celtics",)
    )
    mock_cursor.close.assert_called()

def test_team_stat_display_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Simulate valid input, then 'no' to stop
    inputs = iter(["Lakers", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = [
        (1, "Los Angeles Lakers", "52-30", "30-11", "22-19")
    ]

    result = teamStatDisplay(mock_connection)
    assert result is True
    mock_cursor.execute.assert_called()
    mock_cursor.close.assert_called()

def test_team_stat_display_not_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    inputs = iter(["Atlantis Dream"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = []

    result = teamStatDisplay(mock_connection)
    assert result is False
    mock_cursor.execute.assert_called()
    mock_cursor.close.assert_called()

def test_team_stat_display_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Simulate one team input then exit
    inputs = iter(["Lakers", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = [
        (1, "Lakers", "50-32", "30-11", "20-21")
    ]

    result = teamStatDisplay(mock_connection)
    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_team_stat_display_not_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Team not found
    inputs = iter(["UnknownTeam"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = []

    result = teamStatDisplay(mock_connection)
    assert result is False
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_team_stat_display_exit(monkeypatch):
    mock_connection = MagicMock()
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    result = teamStatDisplay(mock_connection)
    assert result is False
