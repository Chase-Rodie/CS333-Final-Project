# tests/unit/test_stats.py

from unittest.mock import patch, MagicMock
from StatScraping import regularStats
from StatScraping import regularStatDisplay
from StatScraping import playoffStatDisplay
from StatScraping import playoffStats



@patch("StatScraping.pd.DataFrame.to_excel")
@patch("StatScraping.requests.get")
def test_regular_stats_success(mock_get, mock_to_excel):
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'resultSet': {
            'headers': ['RANK', 'PLAYER', 'TEAM', 'PTS'],
            'rowSet': [[1, 'LeBron James', 'LAL', 30.2]]
        }
    }
    mock_get.return_value = mock_response

    regularStats()

    mock_get.assert_called_once()
    mock_to_excel.assert_called_once()


@patch("StatScraping.pd.DataFrame.to_excel")
@patch("StatScraping.requests.get")
def test_playoff_stats_success(mock_get, mock_to_excel):
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'resultSet': {
            'headers': ['RANK', 'PLAYER', 'TEAM', 'PTS'],
            'rowSet': [[1, 'Stephen Curry', 'GSW', 31.5]]
        }
    }
    mock_get.return_value = mock_response

    from StatScraping import playoffStats
    playoffStats()

    mock_get.assert_called_once()
    mock_to_excel.assert_called_once()


def test_playoff_stat_display_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Simulate input: player name, then 'no' to exit
    inputs = iter(["Stephen Curry", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Mock DB returns matching player stat
    mock_cursor.fetchall.return_value = [
        (1, "Stephen Curry", "GSW", 31.2, 5.1, 6.0)
    ]

    result = playoffStatDisplay(mock_connection)

    assert result is True
    mock_cursor.execute.assert_called_with(
        'SELECT "RANK", "PLAYER", "TEAM", "PTS", "REB", "AST" FROM "Playoff Season Stats 22-23" WHERE "PLAYER" ILIKE %s',
        ("Stephen Curry",)
    )
    mock_cursor.close.assert_called()

@patch("StatScraping.requests.get")
def test_regular_stats_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500  # Simulate failure
    mock_get.return_value = mock_response

    regularStats()
    mock_get.assert_called_once()

@patch("StatScraping.requests.get")
def test_playoff_stats_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 403  # Forbidden or similar
    mock_get.return_value = mock_response

    from StatScraping import playoffStats
    playoffStats()
    mock_get.assert_called_once()

def test_playoff_stat_display_not_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Input a name and simulate no DB result
    inputs = iter(["Nonexistent Player"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    mock_cursor.fetchall.return_value = []

    result = playoffStatDisplay(mock_connection)

    assert result is False
    mock_cursor.close.assert_called()

def test_playoff_stat_display_yes_continue(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # User searches once, says "yes", then types "exit" (which skips DB query and exits)
    inputs = iter(["Stephen Curry", "yes", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = [
        (1, "Stephen Curry", "GSW", 31.2, 5.1, 6.0)
    ]

    result = playoffStatDisplay(mock_connection)
    assert result is False
    assert mock_cursor.execute.call_count == 1  # Only one query due to 'exit' on second loop

def test_regular_stat_display_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Simulate player input and 'no' to exit
    inputs = iter(["LeBron James", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = [
        (1, "LeBron James", "LAL", 28.3, 8.1, 7.4)
    ]

    result = regularStatDisplay(mock_connection)
    assert result is True
    mock_cursor.execute.assert_called()
    mock_cursor.close.assert_called()

def test_regular_stat_display_not_found(monkeypatch):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    inputs = iter(["No Name Player"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    mock_cursor.fetchall.return_value = []

    result = regularStatDisplay(mock_connection)
    assert result is False
    mock_cursor.execute.assert_called()
    mock_cursor.close.assert_called()

@patch("StatScraping.requests.get")
def test_playoff_stats_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500  # Simulate failure
    mock_get.return_value = mock_response

    playoffStats()

    mock_get.assert_called_once()

