from fastapi import APIRouter, Depends, HTTPException
from ...models.bet import Bet, BetCreate, BetDB
from ...app.dependencies import get_db
from ...services.odds_service import get_odds  # Import odds service

router = APIRouter()

@router.post("/", response_model=BetDB)
def create_bet(bet: BetCreate, db = Depends(get_db)):
    # In a real application, you'd validate the bet against current odds
    # and user balance.
    return Bet.create(db, bet)

@router.get("/{bet_id}", response_model=BetDB)
def read_bet(bet_id: int, db = Depends(get_db)):
    db_bet = Bet.get(db, bet_id)
    if db_bet is None:
        raise HTTPException(status_code=404, detail="Bet not found")
    return db_bet

@router.get("/odds/")  # Added an endpoint for fetching odds
async def fetch_odds():
    odds_data = get_odds()  # Call your odds service
    return odds_data 