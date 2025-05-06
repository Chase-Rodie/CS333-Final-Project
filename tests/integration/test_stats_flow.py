import os
import psycopg2
import unittest
from StatScraping import loginFunction, regularStatDisplay

class TestStatFlowIntegration(unittest.TestCase):
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
            ('lebron23',)
        )

        # Insert player stat
        self.cursor.execute(
            '''
            INSERT INTO "Regular Season Stats 23-24" ("RANK", "PLAYER", "TEAM", "PTS", "REB", "AST")
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            ''',
            (1, 'LeBron James', 'LAL', 28.5, 7.2, 8.1)
        )

        self.conn.commit()

    def tearDown(self):
        self.cursor.execute('DELETE FROM "User Info" WHERE userid = %s', ('lebron23',))
        self.cursor.execute('DELETE FROM "Regular Season Stats 23-24" WHERE "PLAYER" = %s', ('LeBron James',))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_login_and_stat_display(self):
        # Simulate login input
        input_sequence = iter(['lebron23', 'LeBron James', 'no'])
        original_input = __builtins__.input
        __builtins__.input = lambda _: next(input_sequence)

        try:
            user = loginFunction(self.conn)
            self.assertEqual(user, 'lebron23')

            result = regularStatDisplay(self.conn)
            self.assertTrue(result)
        finally:
            __builtins__.input = original_input

