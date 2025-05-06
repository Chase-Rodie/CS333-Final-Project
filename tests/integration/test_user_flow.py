import os
import psycopg2
import unittest
import builtins
from StatScraping import signupFunction, loginFunction, addFeedback

class TestUserFlowIntegration(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            dbname=os.getenv("DB_NAME", "testdb"),
            user=os.getenv("DB_USER", "testuser"),
            password=os.getenv("DB_PASSWORD", "testpass")
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute('DELETE FROM "User Info" WHERE userid = %s', ('testuser1',))
        self.conn.commit()

    def tearDown(self):
        self.cursor.execute('DELETE FROM "User Info" WHERE userid = %s', ('testuser1',))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_signup_login_add_feedback(self):
        inputs = iter([
            'testuser1',
            'testuser1',
            'I love the stat interface!'
        ])
        original_input = builtins.input
        builtins.input = lambda _: next(inputs)

        try:
            # ---- SIGNUP ----
            user_id = signupFunction(self.conn)
            self.assertEqual(user_id, 'testuser1')

            # ---- LOGIN ----
            logged_in_user = loginFunction(self.conn)
            self.assertEqual(logged_in_user, 'testuser1')

            # ---- ADD FEEDBACK ----
            result = addFeedback(self.conn, 'testuser1')
            self.assertTrue(result)

            # Verify feedback was stored
            self.cursor.execute('SELECT feedback FROM "User Info" WHERE userid = %s', ('testuser1',))
            feedback = self.cursor.fetchone()
            self.assertIsNotNone(feedback)
            self.assertIn('I love the stat interface!', feedback[0])

        finally:
            builtins.input = original_input