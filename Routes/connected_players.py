from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3

#player protocol layout
#---------------------------------------------------------------------
class PlayerState(BaseModel):
    id: str
    x: float
    y: float
    anim: str
    is_attacking: bool = False  # Set a default value
#---------------------------------------------------------------------

route = APIRouter()
# Store all active player connections
active_players = {}
last_known_states = {}

# Broad cast out to other players connected to the server
async def broadcast_to_others(sender_id: str, message_dict: dict):
    last_known_states[sender_id] = message_dict

    dead = []
    for p_id, socket in active_players.items():
        if p_id == sender_id:
            continue
        try:
            await socket.send_json({"id": sender_id, "data": message_dict})
        except Exception:
            dead.append(p_id)

    for p_id in dead:
        active_players.pop(p_id, None)
        last_known_states.pop(p_id, None)
        # also notify others that this player is gone
        await broadcast_leave(p_id)


async def broadcast_leave(leaver_id: str):
    dead = []
    for p_id, socket in active_players.items():
        if p_id == leaver_id:
            continue
        try:
            await socket.send_json({"type": "leave", "id": leaver_id})
        except Exception:
            dead.append(p_id)  # socket is dead too

    # clean up any dead sockets we discovered
    for p_id in dead:
        active_players.pop(p_id, None)
        last_known_states.pop(p_id, None)

def set_user_inactive_by_id(user_id: str):
    db = sqlite3.connect("DataBases/userdata.db")
    cur = db.cursor()
    cur.execute("UPDATE userdata SET is_active = 0 WHERE id = ?", (user_id,))
    db.commit()
    db.close()



@route.websocket("/ws/world/{player_id}")
async def world_socket(websocket: WebSocket, player_id: str):
    player_id = str(player_id)
    await websocket.accept()

    # Send existing players to new client
    for pid, state in last_known_states.items():
        if pid != player_id:
            await websocket.send_json({"id": pid, "data": state})


    active_players[player_id] = websocket

    try:
        while True:
            raw_data = await websocket.receive_json()
            state = PlayerState(**raw_data)
            await broadcast_to_others(player_id, state.model_dump())

    except WebSocketDisconnect:
        pass
    
    except Exception as e:
        # Unexpected server-side error
        print(f"World WS error for {player_id}: {e}")

    finally:
        # cleanup here
        active_players.pop(player_id, None)
        last_known_states.pop(player_id, None)

        try:
            set_user_inactive_by_id(player_id)
        except Exception as e:
            print(f"Failed to set inactive for {player_id}: {e}")

        try:
            await broadcast_leave(player_id)
        except Exception:
            pass
