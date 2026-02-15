from fastapi import FastAPI, Path, Query, HTTPException, Body
from Routes import login, register, chat_ws, connected_players
from pydantic import BaseModel, Field
import sqlite3
import bcrypt


app = FastAPI()


class UserChat(BaseModel):
    name: str
    text: str

current_chat = ""

# Refactored code
# after playing around moved on to how modules will work in fast api
# made folders to house my code per type of request making things easier to maintain and read
# moved my data bases to their own folder as well
# Note to self. files and folder location in the modulers are reltive to your main entry point
# NOT your modules location!
app.include_router(login.route)
app.include_router(register.route)


# PS: I updated my chat to websocket lol
app.include_router(chat_ws.route)


# Websocket testing for players. Might update chat using websockets too
app.include_router(connected_players.route)