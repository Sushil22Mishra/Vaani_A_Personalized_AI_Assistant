from query import *

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import bcrypt
from pydantic import BaseModel
import mysql.connector

# Initialize FastAPI app
app = FastAPI()

# CORS middleware to handle cross-origin requests
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up static files and templates
app.mount("/static", StaticFiles(directory="template/static"), name="static")
template_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
templates = Jinja2Templates(directory=template_folder_path)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#Route to serve favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")

# Optional: API route for handling queries
@app.api_route("/process_query", methods=["POST", "OPTIONS"])
async def process_query_endpoint(request: Request):
    try:
        if request.method == "OPTIONS":
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept",
            }
            return JSONResponse(content={"message": "OPTIONS request received"}, media_type="application/json", headers=headers)
        else:
            user_query = await request.json()
            response = process_query(user_query["query"])
            return {"response": response}
    except Exception as e:
        return {"error": str(e)}

# Database connection configuration
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'your_database'
}

# Model for receiving user data
class UserRegister(BaseModel):
    name: str
    password: str
    profile_pic: str  # Base64 image string

# API to handle user registration
@app.post("/register")
def register_user(user: UserRegister):
    try:
        # Hash the password before storing
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert user data into MySQL
        cursor.execute(
            "INSERT INTO users (name, password, profile_pic) VALUES (%s, %s, %s)",
            (user.name, hashed_password.decode('utf-8'), user.profile_pic)
        )
        connection.commit()

        return {"message": "User  registered successfully!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# To run the FastAPI server, use the command:
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload