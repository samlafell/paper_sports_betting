# backend/app/websocket.py
# Example WebSocket implementation (using FastAPI's WebSocket support)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

connected_clients: List[WebSocket] = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process incoming data (e.g., bet placement, odds updates)
            await websocket.send_text(f"Message text was: {data}")

            # Example: Broadcast odds updates to all connected clients
            # for client in connected_clients:
            #   await client.send_json({"type": "odds_update", "data": ...})
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

# Function to broadcast messages to all connected clients
async def broadcast_message(message: dict):
    for client in connected_clients:
        await client.send_json(message) 