import pytest
import sqlite3


@pytest.fixture
def sqlite_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL)"""
    )

    cursor.executemany(
        """
            INSERT INTO users (username, email) VALUES (?, ?)
        """,
        [("user1", "user1@example.com"), ("user2", "user2@example.com")],
    )
    conn.commit()
    return conn


def test_example(sqlite_db):
    cursor = sqlite_db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    assert len(users) == 2
    assert users[0] == (1, "user1", "user1@example.com")
    assert users[1] == (2, "user2", "user2@example.com")
