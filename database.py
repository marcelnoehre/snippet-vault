import os
import sqlite3
from cryptography.fernet import Fernet
from logger import Logger

class SecureSnippetsDB:
    def __init__(self, db_path=None):
        self._logger = Logger()
        self.db_path = db_path or os.path.expanduser("~/snip_vault.db")
        self._key_path = os.path.expanduser("~/.secure_snippet_key")
        self._key = self._load_key()
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as _connection:
            _connection.cursor().execute("""
                CREATE TABLE IF NOT EXISTS snippets (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    data TEXT
                )
            """)
            _connection.commit()
            self._logger.log(f"Database Initialized at '{self.db_path}'")
    
    def _load_key(self):
        if not os.path.exists(self._key_path):
            _key = Fernet.generate_key()
            with open(self._key_path, "wb") as _file:
                _file.write(_key)
        else:
            with open(self._key_path, "rb") as _file:
                _key = _file.read()
        return Fernet(_key)
    
    def add_snippet(self, name, data):
        with sqlite3.connect(self.db_path) as _connection:
            _cursor = _connection.cursor()
            _cursor.execute("""
                SELECT 1 FROM snippets WHERE name = ?
            """, (name,))
        if _cursor.fetchone():
            self._logger.log(f"Snippet '{name}' already exists")
        else:
            _cursor.execute("""
                INSERT OR REPLACE INTO snippets (name, data) VALUES (?, ?)
            """, (name, self._key.encrypt(data.encode()).decode()))
            self._logger.log(f"Stored Snippet '{name}'")
