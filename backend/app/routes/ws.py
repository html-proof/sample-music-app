from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.websocket_manager import manager
from app.auth_utils import get_current_user_ws

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # In a real app, validate token via query param or headers if possible in WS
    # For now, we assume client_id is the uid or we pass a token in query
    # user = await get_current_user_ws(websocket) # This would be the secure way
    
    # Check for check_token param or similar?
    # For simplicity in this demo, we accept connection and rely on the client sending an auth init message
    # or just trust the client_id for this rapid prototype phase (NOT SECURE for prod)
    
    # Ideally:
    # token = websocket.query_params.get("token")
    # uid = verify_token(token)
    
    uid = client_id # Placeholder for verified UID
    
    await manager.connect(websocket, uid)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages (e.g., "ping", "update_state")
            # await manager.send_personal_message(f"You wrote: {data}", uid)
            pass
    except WebSocketDisconnect:
        manager.disconnect(websocket, uid)
