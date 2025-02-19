from fastapi import FastAPI
from .api import users, bets
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from redis import Redis

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Allow frontend origin
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(bets.router, prefix="/api/bets", tags=["bets"])

# --- Redis Subscription (Conceptual Example) ---
async def redis_subscriber():
    redis_client = Redis(host='localhost', port=6379, db=0)  # Use the same connection settings
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('new-registrations')

    while True:
        try:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                data = json.loads(message['data'])
                print(f"Received registration request: {data}")
                # Process the registration (e.g., create user in database)
                # ... your user creation logic here ...

            await asyncio.sleep(0.01)  # Prevent busy-waiting
        except Exception as e:
            print(f"Error in Redis subscriber: {e}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_subscriber())

@app.get("/api")
async def root():
    return {"message": "Welcome to the Paper Betting API"} 