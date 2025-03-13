#!/usr/bin/env python3

import argparse
import os
import sqlite3
from cryptography.fernet import Fernet

class Logger:
    def __init__(self):
        self._name = "SnipVault"
        self._bold_cyan = "\x1b[36;1m"
        self._bold_yellow = "\x1b[33;1m"
        self._bold_red = "\x1b[31;1m"
        self._white = "\x1b[37;20m"
        self._reset = "\x1b[0m"

    def log(self, msg):
        print("🗂️ " + self._bold_cyan + self._name + self._reset + self._white + ": " + msg)

    def warn(self, msg):
        print("🔔 " + self._bold_yellow + self._name + self._reset + self._white + ": " + msg)

    def error(self, msg):
        print("🚨" + self._bold_red + self._name + self._reset + self._white + ": " + msg)

class SecureSnippetsDB:
    def __init__(self, db_path=None):
        self._logger = Logger()
        self.db_path = db_path or os.path.expanduser("~/snip_vault.db")
        self._key_path = os.path.expanduser("~/.secure_snippet_key")
        self._key = self._load_key()
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as _connection:
            _cursor = _connection.cursor()
            _cursor.execute("""
                CREATE TABLE IF NOT EXISTS snippets (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    data TEXT
                )
            """)
            _connection.commit()
    
    def _load_key(self):
        if not os.path.exists(self._key_path):
            _key = Fernet.generate_key()
            with open(self._key_path, "wb") as _file:
                _file.write(_key)
        else:
            with open(self._key_path, "rb") as _file:
                _key = _file.read()
        return Fernet(_key)

    def save_snippet(self, name, data):
        with sqlite3.connect(self.db_path) as _connection:
            _cursor = _connection.cursor()
            _cursor.execute("""
                SELECT 1 FROM snippets WHERE name = ?
            """, (name,))
            if _cursor.fetchone():
                self._logger.warn(f"Snippet '{name}' already exists")
            else:
                _cursor.execute("""
                    INSERT OR REPLACE INTO snippets (name, data) VALUES (?, ?)
                """, (name, self._key.encrypt(data.encode()).decode()))
                _connection.commit()
                self._logger.log(f"Stored Snippet '{name}'")

    def get_snippet(self, name):
        with sqlite3.connect(self.db_path) as _connection:
            _cursor = _connection.cursor()
            _cursor.execute("""
                SELECT data FROM snippets WHERE name = ?
            """, (name,))
            _data = _cursor.fetchone()
            
        if _data:
            self._logger.log(self._key.decrypt(_data[0].encode()).decode())
        else:
            self._logger.warn(f"Snippet '{name}' not found")
        
    def update_snippet(self, name, data):
        with sqlite3.connect(self.db_path) as _connection:
            _cursor = _connection.cursor()
            _cursor.execute("""
                UPDATE snippets SET data = ? WHERE name = ?
            """, (self._key.encrypt(data.encode()).decode(), name))
            if _cursor.rowcount > 0:
                _connection.commit()
                self._logger.log(f"Updated Snippet '{name}'")
            else:
                self._logger.warn(f"Snippet '{name}' not found")

    def delete_snippet(self, name):
        with sqlite3.connect(self.db_path) as _connection:
            _cursor = _connection.cursor()
            _cursor.execute("""
                DELETE FROM snippets WHERE name = ?
            """, (name,))
            if _cursor.rowcount > 0:
                self._logger.log(f"Deleted Snippet '{name}'")
            else:
                self._logger.warn(f"Snippet '{name}' not found")

    def delete_all_snippets(self):
        with sqlite3.connect(self.db_path) as _connection:
            _cursor = _connection.cursor()
            _cursor.execute("""
                DELETE FROM snippets
            """)
            self._logger.log("Deleted all Snippets")

    def list_snippets(self):
        with sqlite3.connect(self.db_path) as _connection:
            _cursor = _connection.cursor()
            _cursor.execute("""
                SELECT name FROM snippets
            """)
            _snippets = _cursor.fetchall()
            if _snippets:
                self._logger.log("Snippets: " + ", ".join([_snippet[0] for _snippet in _snippets]))
            else:
                self._logger.warn("No Snippets found") 

def _check_params(args, logger):
    if args.action not in ["save", "get", "update", "delete", "clear", "list"]:
        logger.error("Invalid action")
        return False
    elif args.action in ["get", "delete"] and not args.name:
        logger.error(f"Name is required for {args.action} action")
        return False
    elif args.action in ["save", "update"] and (not args.name or not args.value):
        logger.error(f"Name and value are required for {args.action} action")
        return False
    return True

def main():
    _db = SecureSnippetsDB()
    _logger = Logger()

    parser = argparse.ArgumentParser(description="SnipVault")
    parser.add_argument("action", choices=["save", "get", "update", "delete", "clear", "list"], help="Action to perform")
    parser.add_argument("name", nargs="?", default=None, help="Snippet name")
    parser.add_argument("value", nargs="?", default=None, help="Snippet value")
    
    args = parser.parse_args()
    if not _check_params(args, _logger):
        return

    {
        "save": lambda: _db.save_snippet(args.name, args.value),
        "get": lambda: _db.get_snippet(args.name),
        "update": lambda: _db.update_snippet(args.name, args.value),
        "delete": lambda: _db.delete_snippet(args.name),
        "clear": lambda: _db.delete_all_snippets(),
        "list": lambda: _db.list_snippets()
    }[args.action]()

if __name__ == "__main__":
    main()