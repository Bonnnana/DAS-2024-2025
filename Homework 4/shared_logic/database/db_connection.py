"""
 Provides a Singleton implementation for managing a thread-local SQLite database connection.
"""

import sqlite3
import os
from threading import Lock, local

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'all_issuers_data.db'))


class DatabaseConnection:
    _instance = None
    _lock = Lock()
    _thread_local = local()

    def __new__(cls):

        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._conn = None
        return cls._instance

    def get_connection(self):
        if not hasattr(self._thread_local, "connection"):
            try:
                self._thread_local.connection = sqlite3.connect(DB_PATH, check_same_thread=False)
                self._thread_local.connection.row_factory = sqlite3.Row
                print("Database connection established successfully.")
            except sqlite3.Error as e:
                print(f"Error connecting to the database: {e}")
                self._thread_local.connection = None
        return self._thread_local.connection

    def close_connection(self):
        if hasattr(self._thread_local, "connection") and self._thread_local.connection:
            self._thread_local.connection.close()
            self._thread_local.connection = None
            print("Database connection closed.")
