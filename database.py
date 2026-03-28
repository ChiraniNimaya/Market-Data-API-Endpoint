import sqlite3
from config import DB_PATH
 
MONTHS_IN_YEAR = 12
 
def get_db_connection():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row   
        return connection
    except sqlite3.Error as e:
        raise RuntimeError(f"Error connecting to database at '{DB_PATH}': {e}") from e

def init_db():
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS monthly_data (
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
    except sqlite3.Error as e:
        raise RuntimeError(f"Error initializing database: {e}") from e
    finally:
        conn.close()

def save_monthly_data(symbol: str, monthly_series: dict):
    try:
        rows = [
            (symbol.upper(), date, int(date[:4]), float(values["2. high"]), float(values["3. low"]), int(values["5. volume"]))
            for date, values in monthly_series.items()
        ]
    except (KeyError, ValueError) as e:
        raise ValueError(f"Error in API data source: {e}") from e
    
    conn = get_db_connection()
    try:
        conn.executemany(
            """
            INSERT OR REPLACE INTO monthly_data (symbol, date, year, high, low, volume)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Error saving monthly data: {e}") from e
    finally:
        conn.close()

def get_annual_data(symbol: str, year: int):
    conn = get_db_connection()
    try:
        count_row = conn.execute(
            """
            SELECT COUNT(*) as count
            FROM monthly_data
            WHERE symbol = ? AND year = ?
            """,
            (symbol.upper(), year),
        ).fetchone()

        if count_row["count"] < MONTHS_IN_YEAR:
            return None
    
        row = conn.execute(
            """
            SELECT
                MAX(high) AS max_high,
                MIN(low)  AS min_low,
                SUM(volume) AS annual_volume
            FROM monthly_data
            WHERE symbol = ? AND year = ?
            """,
            (symbol.upper(), year),
        ).fetchone()
    
        if row["max_high"] is None:
            return None
 
        return {
            "symbol":      symbol.upper(),
            "year":        year,
            "max_high": row["max_high"],
            "min_low":  row["min_low"],
            "annual_volume": row["annual_volume"]
        }
    except sqlite3.Error as e:
        raise RuntimeError(f"Error Calculating annual data: {e}") from e
    finally:
        conn.close()
	