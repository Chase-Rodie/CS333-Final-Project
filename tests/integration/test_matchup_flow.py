import os
import psycopg2
import unittest
from StatScraping import loginFunction, matchupStatDisplay

class TestMatchupIntegration(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            database=os.getenv("DB_NAME", "testdb"),
            user=os.getenv("DB_USER", "testuser"),
            password=os.getenv("DB_PASSWORD", "testpass")
        )
        self.cursor = self.conn.cursor()

        # Insert test user
        self.cursor.execute("INSERT INTO \"User Info\" (userid) VALUES ('courtVision') ON CONFLICT DO NOTHING")
        self.conn.commit()

        # Insert test matchup data
        self.cursor.execute("""
            INSERT INTO "Matchup Schedule" ("Date", "Visitor/Neutral", "Home/Neutral", "Arena", "Winner")
            VALUES ('Wed Apr 24 2024', 'BOS', 'MIA', 'TD Garden', 'BOS')
            ON CONFLICT DO NOTHING
        """)
        self.conn.commit()

    def tearDown(self):
        self.cursor.execute("DELETE FROM \"User Info\" WHERE userid = 'courtVision'")
        self.cursor.execute("DELETE FROM \"Matchup Schedule\" WHERE \"Date\" = 'Wed Apr 24 2024'")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_login_and_matchup_display(self):
        # Simulate login
        os.environ["PYTHON_INPUT"] = "courtVision"  # Not standard; monkeypatch or refactor if needed

        user = loginFunction(self.conn)
        self.assertEqual(user, 'courtVision')

        # Simulate matchup display
        result = matchupStatDisplay(self.conn)
        self.assertTrue(result)

