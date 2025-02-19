from ..database.database import connection
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import crud, schemas  # Import your CRUD functions and schemas
from jose import JWTError, jwt
from redis import Redis
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Adjust tokenUrl if needed

SECRET_KEY = "your-secret-key"  # Replace with a strong secret key
ALGORITHM = "HS256"

def get_redis():  # <--- Define get_redis *before* get_current_user
    redis_client = Redis(host='localhost', port=6379, db=0)  # Adjust host/port if needed
    try:
        yield redis_client
    finally:
        redis_client.close()

def get_current_user(token: str = Depends(oauth2_scheme), redis_client: Redis = Depends(get_redis)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # --- Redis Retrieval ---
    cached_user = redis_client.get(f"user:{token_data.username}")  # Use username as key
    if cached_user:
        return schemas.User(**json.loads(cached_user))

    user = crud.get_user(username=token_data.username) # You'll need to implement get_user
    if user is None:
        raise credentials_exception

    # --- Redis Caching (after fetching from DB) ---
    user_data = json.dumps(user.dict())
    redis_client.set(f"user:{user.id}", user_data, ex=3600)

    return user

def get_db():
    # DuckDB connection persists—cleanup can be handled on app shutdown if needed.
    yield connection 