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
            volume  INTEGER NOT NULL,
            PRIMARY KEY (symbol, date)
        )
    """)
    conn.commit()
    conn.close()

def save_monthly_data(symbol: str, monthly_series: dict):
    rows = [
        (symbol.upper(), date, int(date[:4]), float(values["2. high"]), float(values["3. low"]), int(values["5. volume"]))
        for date, values in monthly_series.items()
    ]
    conn = get_db_connection()
    conn.executemany(
        """
        INSERT OR REPLACE INTO monthly_prices (symbol, date, year, high, low, volume)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    conn.close()

def get_annual_data(symbol: str, year: int):
    conn = get_db_connection()

    count_row = conn.execute(
        """
        SELECT COUNT(*) as count
        FROM monthly_prices
        WHERE symbol = ? AND year = ?
        """,
        (symbol.upper(), year),
    ).fetchone()

    if count_row["count"] < 12:
        conn.close()
        return None
    
    row = conn.execute(
        """
        SELECT
            MAX(high) AS max_high,
            MIN(low)  AS min_low,
            SUM(volume) AS annual_volume
        FROM monthly_prices
        WHERE symbol = ? AND year = ?
        """,
        (symbol.upper(), year),
    ).fetchone()
    conn.close()
 
    if row["max_high"] is None:
        return None
 
    return {
        "symbol":      symbol.upper(),
        "year":        year,
        "max_high": row["max_high"],
        "min_low":  row["min_low"],
        "annual_volume": row["annual_volume"]
    }
	