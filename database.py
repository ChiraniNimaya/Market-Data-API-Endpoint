import sqlite3
from config import DB_PATH
 
 
def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row   
    return connection

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS monthly_prices (
            symbol  TEXT    NOT NULL,
            date    TEXT    NOT NULL,   
            year    INTEGER NOT NULL,
            high    REAL    NOT NULL,
            low     REAL    NOT NULL,
            PRIMARY KEY (symbol, date)
        )
    """)
    conn.commit()
    conn.close()

def save_monthly_data(symbol: str, monthly_series: dict):
    rows = [
        (symbol.upper(), date, int(date[:4]), float(values["2. high"]), float(values["3. low"]))
        for date, values in monthly_series.items()
    ]
    conn = get_db_connection()
    conn.executemany(
        """
        INSERT OR REPLACE INTO monthly_prices (symbol, date, year, high, low)
        VALUES (?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    conn.close()