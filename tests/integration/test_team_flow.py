import os
import psycopg2
import unittest
import builtins
from StatScraping import loginFunction, teamStatDisplay

class TestTeamFlowIntegration(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            dbname=os.getenv("DB_NAME", "testdb"),
            user=os.getenv("DB_USER", "testuser"),
            password=os.getenv("DB_PASSWORD", "testpass")
        )
        self.cursor = self.conn.cursor()

        # Insert test user
        self.cursor.execute(
            'INSERT INTO "User Info" (userid) VALUES (%s) ON CONFLICT DO NOTHING',
            ('nbaFan99',)
        )

        # Insert team stat
        self.cursor.execute(
            '''
            INSERT INTO "Team Stats" ("Rk", "Team", "Overall", "Home", "Road")
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            ''',
            (1, 'Los Angeles Lakers', '52-30', '30-11', '22-19')
        )

        self.conn.commit()

    def tearDown(self):
        self.cursor.execute('DELETE FROM "User Info" WHERE userid = %s', ('nbaFan99',))
        self.cursor.execute('DELETE FROM "Team Stats" WHERE "Team" = %s', ('Los Angeles Lakers',))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_login_and_team_stat_display(self):
        inputs = iter(['nbaFan99', 'Los Angeles Lakers', 'no'])
        original_input = builtins.input
        builtins.input = lambda _: next(inputs)

        try:
            user = loginFunction(self.conn)
            self.assertEqual(user, 'nbaFan99')

            result = teamStatDisplay(self.conn)
            self.assertTrue(result)
        finally:
            builtins.input = original_input



