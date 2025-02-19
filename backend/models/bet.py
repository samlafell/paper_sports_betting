from pydantic import BaseModel

class BetBase(BaseModel):
    user_id: int
    market: str
    outcome: str
    odds: float
    stake: float

class BetCreate(BetBase):
    pass

class BetDB(BetBase):
    id: int
    status: str

    class Config:
        orm_mode = True

# Helper functions for DuckDB
class Bet:
    @staticmethod
    def get(db, bet_id: int):
        result = db.execute("SELECT * FROM bets WHERE id = ?;", (bet_id,)).fetchall()
        if result:
            row = result[0]
            return BetDB(
                id=row[0],
                user_id=row[1],
                market=row[2],
                outcome=row[3],
                odds=row[4],
                stake=row[5],
                status=row[6],
            )
        return None

    @staticmethod
    def create(db, bet: BetCreate):
        db.execute(
            "INSERT INTO bets (user_id, market, outcome, odds, stake, status) VALUES (?, ?, ?, ?, ?, ?);",
            (bet.user_id, bet.market, bet.outcome, bet.odds, bet.stake, "pending")
        )
        new_id = db.execute("SELECT MAX(id) FROM bets;").fetchone()[0]
        return Bet.get(db, new_id) 