from fastapi import FastAPI, Path, Query, HTTPException, Body, APIRouter
from pydantic import BaseModel, Field
import sqlite3
import bcrypt

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

@route.post("/register")
async def LoginRequest(user_data: UserData):
    pwd_hash = get_password_hash(user_data.password)

    db_connect = sqlite3.connect("DataBases/userdata.db")
    cursor = db_connect.cursor()

    cursor.execute(
        "SELECT username FROM userdata WHERE username = ?",(user_data.user_name,)
    )
    # Fetch result
    result = cursor.fetchone() # This only gets 1 row
    
    print(result)
    if result == None:
        cursor.execute(
            "INSERT INTO userdata (id, username, password) VALUES (NULL, ?,?)",
            (user_data.user_name,pwd_hash,)
        )
        db_connect.commit()
        db_connect.close()
        return {
            "user_name": user_data.user_name, 
            "message": f"{user_data.user_name} is now registered", 
            "valid" : True
            }
    else:
        db_connect.close()
        return {
            "user_name": user_data.user_name, 
            "message": f"{user_data.user_name} is already in use", 
            "valid" : False
            }