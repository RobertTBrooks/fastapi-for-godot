from fastapi import FastAPI, Path, Query, HTTPException, Body, APIRouter
from pydantic import BaseModel, Field
import sqlite3
import bcrypt

class LogoutRequest(BaseModel):
    user_name: str

#For logout option
@route.post("/logout")
async def logout(req: LogoutRequest):
    db = sqlite3.connect("DataBases/userdata.db")
    cur = db.cursor()
    cur.execute("UPDATE userdata SET is_active = 0 WHERE username = ?", (req.user_name,))
    db.commit()
    db.close()
    return {"ok": True}
