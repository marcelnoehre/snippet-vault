import os
import sqlite3

class SecureSnippetsDB:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.expanduser("~/snip_vault.db")
        self._connection = sqlite3.connect(self.db_path)
        self._cursor = self._connection.cursor()

    def init_db(self):
        self._connection = sqlite3.connect(self.db_path)
        self._cursor = self._connection.cursor()
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                data TEXT
            )
        """)
        self._connection.commit()
        self._connection.close()