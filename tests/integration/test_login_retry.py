# tests/integration/test_login_retry_integration.py

import psycopg2
from StatScraping import loginFunction

def test_login_retry_real_db(monkeypatch):
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="your_test_db",
        user="your_test_user",
        password="your_test_password"
    )

    cursor = connection.cursor()
    cursor.execute('DELETE FROM "User Info" WHERE userid IN (%s, %s)', ('wronguser', 'gooduser'))
    cursor.execute('INSERT INTO "User Info" (userid) VALUES (%s)', ('gooduser',))
    connection.commit()

    inputs = iter(['wronguser', 'gooduser'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result1 = loginFunction(connection)
    assert result1 is None

    result2 = loginFunction(connection)
    assert result2 == 'gooduser'

    # Cleanup
    cursor.execute('DELETE FROM "User Info" WHERE userid IN (%s, %s)', ('wronguser', 'gooduser'))
    connection.commit()
    cursor.close()
    connection.close()

