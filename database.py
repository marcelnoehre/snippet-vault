import os
import sqlite3
from cryptography.fernet import Fernet

class SecureSnippetsDB:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.expanduser("~/snip_vault.db")
        self._key_path = os.path.expanduser("~/.secure_snippet_key")
        self._key = self._load_key()
        self._init_db()

    def _execute_query(self, query, params=None):
        with sqlite3.connect(self.db_path) as _connection:
            _connection.cursor().execute(query, params or ())
            _connection.commit()
            _connection.close()

    def _init_db(self):
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                data TEXT
            )
        """)
    
    def _load_key(self):
        if not os.path.exists(self._key_path):
            _key = Fernet.generate_key()
            with open(self._key_path, "wb") as _file:
                _file.write(_key)
        else:
            with open(self._key_path, "rb") as _file:
                _key = _file.read()
        return Fernet(_key)
