from fastapi import FastAPI, Path, Query, HTTPException, Body, APIRouter
from pydantic import BaseModel, Field
import sqlite3
import bcrypt

route = APIRouter()

class UserChat(BaseModel):
    name: str
    text: str

current_chat = ""

#fetch chat
@route.get("/current_chat")
async def get_current_chat():
    db_connect = sqlite3.connect("DataBases/chat_data.db")
    cursor = db_connect.cursor()

    # ask for the messages from the DB
    cursor.execute(
        "SELECT message From storage WHERE id = 1"
        )
    
    # Fetch result
    result = cursor.fetchone() # This only gets 1 row

    db_connect.close()

    # result[0] is the "message" string
    return {"text" : result[0]}

@route.get("/")
async def hello_world():
    return {"text": "Hello World!"}

# Update chat
@route.post("/chat")
async def chat(user_chat: UserChat):
    db_connect = sqlite3.connect("DataBases/chat_data.db")
    cursor = db_connect.cursor()

    # ask for the messages from the DB
    cursor.execute(
        "UPDATE storage SET message = ? WHERE id = 1", (user_chat.text,)
        )
    # Save and Close
    db_connect.commit()
    db_connect.close()

    # result[0] is the "message" string
    return {"name" : "Me: ", "text": user_chat.text}