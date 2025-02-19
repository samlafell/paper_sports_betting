from ..models.bet import Bet, BetCreate
from ..models.user import User

def place_bet(db, bet: BetCreate):
    user = User.get(db, bet.user_id)
    if user.balance < bet.stake:
        raise ValueError("Insufficient balance")

    db_bet = Bet.create(db, bet)

    # Update user balance
    new_balance = user.balance - bet.stake
    db.execute("UPDATE users SET balance = ? WHERE id = ?;", (new_balance, bet.user_id))

    return db_bet

def settle_bet(db, bet_id: int, outcome: str):
    bet = Bet.get(db, bet_id)
    if not bet:
        raise ValueError("Bet not found")

    if bet.status != "pending":
        raise ValueError("Bet already settled")

    if bet.outcome == outcome:
        new_status = "won"
        user = User.get(db, bet.user_id)
        winnings = bet.stake * bet.odds
        new_balance = user.balance + winnings
        db.execute("UPDATE users SET balance = ? WHERE id = ?;", (new_balance, bet.user_id))
    else:
        new_status = "lost"

    db.execute("UPDATE bets SET status = ? WHERE id = ?;", (new_status, bet_id))
    return Bet.get(db, bet_id)

# Add functions for getting user bets, calculating potential winnings, etc. 