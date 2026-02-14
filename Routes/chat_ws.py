from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import sqlite3
import json

route = APIRouter()

# ---- connection manager ----------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        text = json.dumps(message)
        for connection in self.active_connections:
            await connection.send_text(text)

manager = ConnectionManager()
#---------------------------------------------------------



@route.websocket("/ws/chat/{player_id}")
async def chat_ws(websocket: WebSocket, player_id: str):
    await manager.connect(websocket)

    # # OPTIONAL: send last message on connect
    # try:
    #     db = sqlite3.connect("DataBases/chat_data.db")
    #     cur = db.cursor()
    #     cur.execute("SELECT message FROM storage WHERE id = 1")
    #     row = cur.fetchone()
    #     db.close()

    #     if row and row[0]:
    #         await websocket.send_text(json.dumps({
    #             "type": "history",
    #             "messages": [{"text": row[0]}]
    #         }))
    # except Exception:
    #     pass

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            # expected:
            # {
            #     "type":"chat",
            #     "id":"123", 
            #     "username": "string",
            #     "text":"hello"
            # }
            
            if data.get("type") != "chat":
                continue

            text = data.get("text", "").strip()
            username = str(data.get("username", "")).strip()

            if text == "":
                continue

            # ---- store message ----
            # Future updates if needed i'll add chat history and append all messages
            # For now just only keep the last message up-to-date.
            db = sqlite3.connect("DataBases/chat_data.db")
            cur = db.cursor()
            cur.execute(
                "UPDATE storage SET message = ? WHERE id = 1",
                (text,)
            )
            db.commit()
            db.close()

            # ---- broadcast to all clients ----
            await manager.broadcast({
                "type": "chat",
                "username": username,
                "id": player_id,
                "text": text
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
