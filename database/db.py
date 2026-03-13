import sqlite3
from settings import settings

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'db_name'):
            self.db_name = settings.db
            self._init_db()

    def get_connection(self):
        """Returns a connection with Row factory for dict-like access."""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Creates the table if it does not exist using raw SQL."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS stock_data (
                    symbol TEXT,
                    year TEXT,
                    high REAL,
                    low REAL,
                    volume INTEGER,
                    PRIMARY KEY (symbol, year)
                )
            """)
            conn.commit()

    def store_annual_record(self, record: dict):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT  INTO stock_data VALUES (?, ?, ?, ?, ?)",
                (
                    record["symbol"],
                    str(record["year"]),
                    record["high"],
                    record["low"],
                    record["volume"]
                )
            )
            conn.commit()

    def get_annual_summary(self, symbol: str, year: int) -> dict:
        """Retrieves aggregated annual data using SQL functions."""
        query = """
            SELECT 
                high, 
                low, 
                volume 
            FROM stock_data 
            WHERE symbol = ? AND year = ?
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (symbol.upper(), year))
            row = cursor.fetchone()
            
            # If no data is found, MAX(high) will be None
            if row and row["high"] is not None:
                return dict(row)
            return None
