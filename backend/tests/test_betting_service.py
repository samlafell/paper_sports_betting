import pytest
import duckdb
from ..services.betting_service import place_bet, settle_bet
from ..models.user import User, UserCreate
from ..models.bet import BetCreate

TEST_DATABASE_PATH = ":memory:"

@pytest.fixture(scope="module")
def db():
    connection = duckdb.connect(database=TEST_DATABASE_PATH, read_only=False)
    connection.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR UNIQUE,
        hashed_password VARCHAR,
        balance FLOAT DEFAULT 1000.0
    );
    """)
    connection.execute("""
    CREATE TABLE bets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        market VARCHAR,
        outcome VARCHAR,
        odds FLOAT,
        stake FLOAT,
        status VARCHAR DEFAULT 'pending'
    );
    """)
    yield connection
    connection.close()

@pytest.fixture(scope="function")
def test_user(db):
    user_data = UserCreate(username="testuser", password="testpassword")
    user = User.create(db, user_data)
    yield user
    db.execute("DELETE FROM users WHERE id = ?;", (user.id,))
    db.commit()

def test_place_bet(db, test_user):
    bet_data = BetCreate(user_id=test_user.id, market="Test Market", outcome="Test Outcome", odds=2.0, stake=10.0)
    bet = place_bet(db, bet_data)
    assert bet.user_id == test_user.id
    assert bet.status == "pending"
    assert test_user.balance == 990.0  # Check balance update

def test_settle_bet_won(db, test_user):
    bet_data = BetCreate(user_id=test_user.id, market="Test Market", outcome="Test Outcome", odds=2.0, stake=10.0)
    bet = place_bet(db, bet_data)
    settled_bet = settle_bet(db, bet.id, "Test Outcome")
    assert settled_bet.status == "won"
    assert test_user.balance == 990.0 + (10.0 * 2.0)  # Check balance update

def test_settle_bet_lost(db, test_user):
    bet_data = BetCreate(user_id=test_user.id, market="Test Market", outcome="Test Outcome", odds=2.0, stake=10.0)
    bet = place_bet(db, bet_data)
    settled_bet = settle_bet(db, bet.id, "Other Outcome")
    assert settled_bet.status == "lost"
    assert test_user.balance == 990.0 # Check balance update (no winnings)

def test_place_bet_insufficient_balance(db, test_user):
    bet_data = BetCreate(user_id=test_user.id, market="Test Market", outcome="Test Outcome", odds=2.0, stake=10000.0)
    with pytest.raises(ValueError):
        place_bet(db, bet_data)

def test_settle_bet_not_found(db):
    with pytest.raises(ValueError):
        settle_bet(db, 9999, "Test Outcome") # Non-existent bet ID

def test_settle_bet_already_settled(db, test_user):
    bet_data = BetCreate(user_id=test_user.id, market="Test Market", outcome="Test Outcome", odds=2.0, stake=10.0)
    bet = place_bet(db, bet_data)
    settle_bet(db, bet.id, "Test Outcome")  # Settle once
    with pytest.raises(ValueError):
        settle_bet(db, bet.id, "Test Outcome")  # Try to settle again 