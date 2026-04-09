import sqlite3
import json
import time
from core.config import Config

class CacheEngine:
    """High-performance SQLite caching for network requests."""
    
    def __init__(self):
        self.db_path = Config.CACHE_DB
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp REAL
                )
            ''')
            conn.commit()

    def get(self, key: str, ttl: int = None):
        """Retrieve a value from cache if it hasn't expired."""
        if ttl is None:
            ttl = Config.CACHE_TTL
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT value, timestamp FROM cache WHERE key=?', (key,))
                row = cursor.fetchone()
                
                if row:
                    value_json, ts = row
                    if time.time() - ts < ttl:
                        return json.loads(value_json)
                    else:
                        # Auto-cleanup expired record
                        conn.execute('DELETE FROM cache WHERE key=?', (key,))
                        conn.commit()
        except Exception:
            pass
        return None

    def set(self, key: str, value: dict):
        """Store a value in cache with current timestamp."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    'INSERT OR REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)',
                    (key, json.dumps(value), time.time())
                )
                conn.commit()
        except Exception:
            pass

    def clear(self):
        """Wipe the entire cache."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM cache')
                conn.commit()
        except Exception:
            pass

# Global instance
cache_engine = CacheEngine()
