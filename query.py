import datetime
import webbrowser
import pyautogui
from fuzzywuzzy import process
import random
import re
import math

# Function for opening apps
def openApp(appName):
    pyautogui.press('win')
    pyautogui.typewrite(appName)
    pyautogui.press('enter')

# Predefined commands and their responses
COMMANDS = {
    "hello": "Hi, I am Vaani! What can I help you with?",
     # Popular Websites
    "google": lambda: (webbrowser.open("https://google.com"), "Opening Google..."),
    "github": lambda: (webbrowser.open("https://github.com"), "Opening GitHub..."),
    "youtube": lambda: (webbrowser.open("https://youtube.com"), "Opening YouTube..."),
    "linkedin": lambda: (webbrowser.open("https://www.linkedin.com"), "Opening LinkedIn..."),
    "instagram": lambda: (webbrowser.open("https://instagram.com"), "Opening Instagram..."),
    "facebook": lambda: (webbrowser.open("https://facebook.com"), "Opening Facebook..."),
    "twitter": lambda: (webbrowser.open("https://twitter.com"), "Opening Twitter..."),
    "reddit": lambda: (webbrowser.open("https://reddit.com"), "Opening Reddit..."),
    "pinterest": lambda: (webbrowser.open("https://pinterest.com"), "Opening Pinterest..."),
    "gmail": lambda: (webbrowser.open("https://gmail.com"), "Opening Gmail..."),
    "whatsapp": lambda: (webbrowser.open("https://web.whatsapp.com"), "Opening WhatsApp..."),
    "telegram": lambda: (webbrowser.open("https://web.telegram.org"), "Opening Telegram..."),
    "discord": lambda: (webbrowser.open("https://discord.com"), "Opening Discord..."),
    
    # Entertainment & Streaming
    "netflix": lambda: (webbrowser.open("https://netflix.com"), "Opening Netflix..."),
    "amazon prime": lambda: (webbrowser.open("https://www.primevideo.com"), "Opening Amazon Prime Video..."),
    "hotstar": lambda: (webbrowser.open("https://www.hotstar.com"), "Opening Hotstar..."),
    "spotify": lambda: (webbrowser.open("https://open.spotify.com"), "Opening Spotify..."),
    
    # Cloud Storage
    "google drive": lambda: (webbrowser.open("https://drive.google.com/drive/my-drive"), "Opening Google Drive..."),
    "dropbox": lambda: (webbrowser.open("https://dropbox.com"), "Opening Dropbox..."),
    "onedrive": lambda: (webbrowser.open("https://onedrive.live.com"), "Opening OneDrive..."),
    
    # Productivity & Learning
    "stack overflow": lambda: (webbrowser.open("https://stackoverflow.com"), "Opening Stack Overflow..."),
    "notion": lambda: (webbrowser.open("https://notion.so"), "Opening Notion..."),
    "zoom": lambda: (webbrowser.open("https://zoom.us"), "Opening Zoom..."),
    "chatgpt": lambda: (webbrowser.open("https://chat.openai.com"), "Opening ChatGPT..."),
    "coursera": lambda: (webbrowser.open("https://coursera.org"), "Opening Coursera..."),
    "edu plus": lambda: (webbrowser.open("https://mauli.edupluscampus.com"), "Opening Edu Plus Login Page..."),
    "university result": lambda: (webbrowser.open("https://sgbau.ucanapply.com/"), "You can check the results here..."),
    "sgbau": lambda: (webbrowser.open("https://sgbau.ucanapply.com/"), "You can check the results here..."),

    # Utility Commands
    "time": lambda: f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}",
    "weather": lambda: (webbrowser.open("https://www.google.com/search?q=weather"), "Here is the weather update..."),
    "news": lambda: (webbrowser.open("https://news.google.com"), "Here are the latest news updates..."),
    "calculator": lambda: (webbrowser.open("https://www.google.com/search?q=calculator"), "Opening Calculator..."),
    "calendar": lambda: (webbrowser.open("https://calendar.google.com"), "Opening Google Calendar..."),

    # Food & Shopping
    "restaurant": lambda: (webbrowser.open("https://google.com/search?q=restaurants near me"), "Searching for restaurants near you..."),
    "online shopping": lambda: (webbrowser.open("https://google.com/search?q=online shopping"), "You can shop online from these websites..."),
    "amazon": lambda: (webbrowser.open("https://amazon.com"), "Opening Amazon..."),
    "flipkart": lambda: (webbrowser.open("https://www.flipkart.com"), "Opening Flipkart..."),
    "myntra": lambda: (webbrowser.open("https://www.myntra.com"), "Opening Myntra..."),
    "zomato": lambda: (webbrowser.open("https://www.zomato.com"), "Opening Zomato..."),
    "swiggy": lambda: (webbrowser.open("https://www.swiggy.com"), "Opening Swiggy..."),

}

# Function to process user queries
def process_query(user_query):
    user_query = user_query.lower().strip()

    # Handling app launch separately
    if "launch" in user_query:
        app_name = user_query.replace("launch", "").strip()
        openApp(app_name)
        return f"Opening {app_name}..."
    
    # Handling search queries
    if "search" in user_query:
        search_term = user_query.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        return f"Here is what I found for {search_term}"
    
    if "wikipedia for" in user_query:
        search_term = user_query.replace("wikipedia for", "").strip()
        webbrowser.open(f"https://en.wikipedia.org/wiki/{search_term}")
        return f"Here is what I found on Wikipedia for {search_term}"
    
    if "where is" in user_query:
        location = user_query.replace("where is", "").strip()
        webbrowser.open(f"https://www.google.com/maps/search/{location}")
        return f"Here is {location} on Google Maps"
    

    # Function to extract number from query
    def extract_number(query, keyword):
        match = re.search(rf"{keyword} (\d+)", query)
        return int(match.group(1)) if match else None
    
    # Square Calculation
    if "square of" in user_query:
        number = extract_number(user_query, "square of")
        if number is not None:
            result = number ** 2
            return f"The square of {number} is = {result}"
        else:
            return "Please provide a valid number."

    # Cube Calculation
    if "cube of" in user_query:
        number = extract_number(user_query, "cube of")
        if number is not None:
            result = number ** 3
            return f"The cube of {number} is = {result}"
        else:
            return "Please provide a valid number."
    
    # Square Root Calculation
    if "square root of" in user_query:
        number = extract_number(user_query, "square root of")
        if number is not None:
            result = math.sqrt(number)
            return f"The square root of {number} is = {result:.2f}"
        else:
            return "Please provide a valid number."

    # General Calculation
    if "calculate" in user_query:
        expression = re.sub(r"[^0-9+\-*/(). x]", "", user_query.replace("calculate", "").strip())
        expression = expression.replace("x", "*")  # Convert 'x' to '*'

        if re.match(r'^[0-9+\-*/(). ]+$', expression):  # Allow only valid operators
            try:
                result = eval(expression)
                return f"The result of {expression} is = {result}"
            except:
                return "Sorry, I couldn't calculate that."
        else:
            return "Invalid input. Please enter a valid mathematical expression."

    
    # Fuzzy match user query with predefined commands
    match, confidence = process.extractOne(user_query, COMMANDS.keys())
    
    if confidence > 80:
        response = COMMANDS[match]
        if callable(response):
            _, message = response()
            return message
        return response
    
    # Default action: Google search
    webbrowser.open(f"https://www.google.com/search?q={user_query}")
    return f"Here is what I found for {user_query}"