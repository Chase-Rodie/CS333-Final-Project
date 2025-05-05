# tests/unit/test_database.py

import sys
import psycopg2
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from StatScraping import connect_to_database
from unittest.mock import patch, MagicMock

@patch('psycopg2.connect')
def test_connect_to_database_success(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    conn = connect_to_database()
    assert conn == mock_conn
    mock_connect.assert_called_once()

@patch('psycopg2.connect', side_effect=psycopg2.Error("DB fail"))
def test_connect_to_database_failure(mock_connect):
    conn = connect_to_database()
    assert conn is None
    mock_connect.assert_called_once()

