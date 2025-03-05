from query import *
from database_route import insert_user, get_user_by_name
import os
import webbrowser
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import bcrypt
from pydantic import BaseModel
import mysql.connector
import uvicorn

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

# Model for receiving user data
class UserRegister(BaseModel):
    name: str
    password: str
    profile_pic: str  # Base64 image string

# Model for receiving login data
class UserLogin(BaseModel):
    name: str
    password: str

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})  # Serve home.html

@app.get("/services")
async def services_page(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})  # Serve services.html

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})  # Serve login.html

@app.post("/login")
async def login_user(user: UserLogin):
    db_user = get_user_by_name(user.name)  # Call the function to fetch user data
    if db_user is None or not bcrypt.checkpw(user.password.encode('utf-8'), db_user['password'].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Redirect to vaani.html upon successful login
    return RedirectResponse(url="/vaani", status_code=303)

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})  # Serve register.html

@app.post("/register")
async def register_user(
    name: str = Form(...),
    password: str = Form(...),
    profile_pic: UploadFile = File(None)  # Accepting an image file
):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Read image data
        profile_pic_data = await profile_pic.read() if profile_pic else None

        # Insert user data into MySQL
        insert_user(name, hashed_password.decode('utf-8'), profile_pic_data)

        #  Return a redirect response to the frontend
        return RedirectResponse(url="/vaani", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vaani")
async def vaani_page(request: Request):
    return templates.TemplateResponse("vaani.html", {"request": request})  # Serve vaani.html

# Route to serve favicon
@app.get("/favicon.ico")
async def favicon():
    if os.path.exists("favicon.ico"):
        return FileResponse("favicon.ico")
    else:
        return JSONResponse(content={"message": "Favicon not found"}, status_code=404)

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
    'user': 'root',          # Ensure this is 'root'
    'password': 'system',    # Ensure this matches the password you set
    'host': 'localhost',
    'database': 'vaani_database'
}

def start_server():
    # Start the server without reload
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Open the browser to the home page
    webbrowser.open("http://127.0.0.1:8000")
    start_server()  # Start the server