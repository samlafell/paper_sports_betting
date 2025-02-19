import duckdb

# Connect to a DuckDB file-based database (or use ":memory:" for an in-memory DB)
connection = duckdb.connect(database="paper_betting.duckdb", read_only=False)

# Create tables if they don't exist
connection.execute("""
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR UNIQUE,
  hashed_password VARCHAR,
  balance FLOAT DEFAULT 1000.0
)
""")

connection.execute("""
CREATE TABLE IF NOT EXISTS bets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  market VARCHAR,
  outcome VARCHAR,
  odds FLOAT,
  stake FLOAT,
  status VARCHAR DEFAULT 'pending'
)
""") 