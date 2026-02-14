from fastapi import FastAPI, Path, Query, HTTPException, Body, APIRouter
from pydantic import BaseModel, Field
import sqlite3
import bcrypt
import time, secrets

route = APIRouter()

class UserData(BaseModel):
    user_name: str
    password: str

#Function helpers
#--------------------------------------------------------------------
# Function to turn a plain password into a hash
def get_password_hash(password: str):
    # 1. Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Generate a 'salt' and hash it
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # 3. Return as a string to save in SQLite
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    # Compare the plain text attempt with the stored hash
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

#--------------------------------------------------------------------

@route.post("/login")
async def login(user_data: UserData):
    TIMEOUT = 20  # seconds
    now = int(time.time())
    session_id = secrets.token_hex(16)

    db = sqlite3.connect("DataBases/userdata.db")
    cur = db.cursor()

    try:
        cur.execute("BEGIN IMMEDIATE")

        # IMPORTANT: select last_seen + session_id
        cur.execute("""
            SELECT id, password, is_active, last_seen
            FROM userdata
            WHERE username = ?
        """, (user_data.user_name,))
        row = cur.fetchone()

        if row is None:
            db.rollback()
            return {
                "user_name": user_data.user_name,
                "message": "Account not found",
                "valid": False
            }

        user_id, stored_pass, is_active, last_seen = row

        if not verify_password(user_data.password, stored_pass):
            db.rollback()
            return {
                "user_name": user_data.user_name,
                "message": "Incorrect password",
                "valid": False
            }

        # Block only if session is still fresh
        if int(is_active) == 1 and (now - int(last_seen)) <= TIMEOUT:
            db.rollback()
            return {
                "user_name": user_data.user_name,
                "message": f"{user_data.user_name} is already logged in.",
                "valid": False,
                "already_logged_in": True
            }

        # Create / refresh session
        cur.execute("""
            UPDATE userdata
            SET is_active = 1,
                session_id = ?,
                last_seen = ?
            WHERE id = ?
        """, (session_id, now, user_id))

        db.commit()

        return {
            "id": user_id,
            "user_name": user_data.user_name,
            "session_id": session_id,
            "valid": True,
            "message": f"Welcome back {user_data.user_name}"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()



async def logout(req: LogoutRequest):
    db = sqlite3.connect("DataBases/userdata.db")
    cur = db.cursor()
    cur.execute("UPDATE userdata SET is_active = 0 WHERE username = ?", (req.user_name,))
    db.commit()
    db.close()
    return {"ok": True}