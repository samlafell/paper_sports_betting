from fastapi import APIRouter, Depends, HTTPException, status
from ...models.user import User, UserCreate, UserDB
from ...app.dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm
from ..dependencies import get_current_user  # Assuming you have this
from .. import crud, schemas
from redis import Redis  # Import Redis
import json
from typing import Annotated

router = APIRouter()

# --- Redis Connection (Move to dependencies.py for better structure) ---
def get_redis():
    redis_client = Redis(host='localhost', port=6379, db=0)  # Adjust host/port if needed
    try:
        yield redis_client
    finally:
        redis_client.close()

@router.post("/", response_model=UserDB)
def create_user(user: UserCreate, db = Depends(get_db)):
    db_user = User.get_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return User.create(db, user)

@router.get("/{user_id}", response_model=UserDB)
def read_user(user_id: int, db = Depends(get_db)):
    db_user = User.get(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/token")  # Assuming you have a token endpoint
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), redis_client: Redis = Depends(get_redis)):
    user = crud.authenticate_user(form_data.username, form_data.password) # You'll need to implement authenticate_user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # --- Redis Caching ---
    user_data = json.dumps(user.dict())  # Convert user object to JSON string
    redis_client.set(f"user:{user.id}", user_data, ex=3600)  # Cache for 1 hour (ex=seconds)

    access_token = crud.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user), redis_client: Redis = Depends(get_redis)):

    # --- Redis Retrieval ---
    cached_user = redis_client.get(f"user:{current_user.id}")
    if cached_user:
        return json.loads(cached_user)  # Return cached user data

    # If not in cache, fetch from DB (assuming get_current_user does this)
    # and store in Redis
    user_data = json.dumps(current_user.dict())
    redis_client.set(f"user:{current_user.id}", user_data, ex=3600)
    return current_user

# Add other user-related endpoints (e.g., update_user, delete_user) 