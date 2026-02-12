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

@route.get("/login")
async def LoginRequest(user_data: UserData):
    db_connect = sqlite3.connect("DataBases/userdata.db")
    cursor = db_connect.cursor()

    cursor.execute(
        "SELECT password FROM userdata WHERE username = ?",(user_data.user_name,)
    )
    # Fetch result
    result = cursor.fetchone() # This only gets 1 row
    db_connect.close()
    print(result)
    if result != None:
        stored_pass = result[0]
        is_correct = verify_password(str(user_data.password), stored_pass)
        if is_correct:
            return {
                "user_name": user_data.user_name, 
                "message": f"Welcome back {user_data.user_name}", 
                "valid" : True
                }
        else:
            return {
                "user_name": user_data.user_name, 
                "message": f"Incorrect password for {user_data.user_name}", 
                "valid" : False
                }
    
    if result == None:
        return {
            "user_name": user_data.user_name, 
            "message": f"No account for {user_data.user_name} was found.\nRegister a new account", 
            "valid" : False
            }