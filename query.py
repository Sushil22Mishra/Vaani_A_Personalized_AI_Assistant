import datetime
import webbrowser
import pyautogui
from fuzzywuzzy import process
import mysql.connector
import os
import random
import re
import math
import time
import requests
import threading
from plyer import notification
import psutil
import GPUtil




def setReminder(reminder_text, seconds):
    def reminder():
        time.sleep(seconds)
        notification.notify(
            title="Reminder",
            message=reminder_text,
            timeout=10  # Notification stays for 10 seconds
        )

    threading.Thread(target=reminder, daemon=True).start()
    return f"Reminder set for {seconds} seconds: {reminder_text}"

def get_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        else:
            return None
    except Exception:
        return None


def openApp(appName):
    pyautogui.press('win')  # Opens the Start menu
    time.sleep(0.5)  # Small delay for stability
    pyautogui.typewrite(appName)  # Types the app name
    time.sleep(0.5)  
    pyautogui.press('enter')  # Launches the app)


def close_tab():
    pyautogui.hotkey('ctrl', 'w')
def get_system_info():
    # RAM info
    ram = psutil.virtual_memory()
    ram_total = round(ram.total / (1024 ** 3), 2)  # in GB
    ram_used = round(ram.used / (1024 ** 3), 2)
    ram_percentage = ram.percent

    # Battery info
    battery = psutil.sensors_battery()
    if battery:
        battery_percent = battery.percent
        charging = battery.power_plugged
    else:
        battery_percent = None
        charging = None

    # GPU info
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        gpu_name = gpu.name
        gpu_load = f"{gpu.load*100:.1f}%"
        gpu_memory_total = f"{gpu.memoryTotal}MB"
        gpu_memory_used = f"{gpu.memoryUsed}MB"
    else:
        gpu_name = "No GPU found"
        gpu_load = "N/A"
        gpu_memory_total = "N/A"
        gpu_memory_used = "N/A"

    # Create a response
    info = f"RAM: {ram_used} GB used out of {ram_total} GB ({ram_percentage}%).\n"

    if battery_percent is not None:
        info += f"Battery: {battery_percent}% {'(Charging)' if charging else '(Not Charging)'}.\n"
    else:
        info += "Battery: No battery detected.\n"

    info += f"GPU: {gpu_name}, Load: {gpu_load}, Memory Usage: {gpu_memory_used}/{gpu_memory_total}."

    return info


def read_text_file(file_name):
    file_path = os.path.join("txt", file_name)  # Ensures correct path format
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            return content if content else "The introduction file is empty."
    except FileNotFoundError:
        return "I couldn't find my introduction file."

def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    return filename

    



# Predefined commands and their responses
COMMANDS = {


    "hello": "Hi, I am Vaani! What can I help you with?",
    "hi": "Hi, I am Vaani! What can I help you with?",
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
    "amazonprime": lambda: (webbrowser.open("https://www.primevideo.com"), "Opening Amazon Prime Video..."),
    "hotstar": lambda: (webbrowser.open("https://www.hotstar.com"), "Opening Hotstar..."),
    "spotify": lambda: (webbrowser.open("https://open.spotify.com"), "Opening Spotify..."),
    
    # Cloud Storage
    "googledrive": lambda: (webbrowser.open("https://drive.google.com/drive/my-drive"), "Opening Google Drive..."),
    "dropbox": lambda: (webbrowser.open("https://dropbox.com"), "Opening Dropbox..."),
    "onedrive": lambda: (webbrowser.open("https://onedrive.live.com"), "Opening OneDrive..."),
    
    # Productivity & Learning
    "stackoverflow": lambda: (webbrowser.open("https://stackoverflow.com"), "Opening Stack Overflow..."),
    "notion": lambda: (webbrowser.open("https://notion.so"), "Opening Notion..."),
    "zoom": lambda: (webbrowser.open("https://zoom.us"), "Opening Zoom..."),
    "chatgpt": lambda: (webbrowser.open("https://chat.openai.com"), "Opening ChatGPT..."),
    "coursera": lambda: (webbrowser.open("https://coursera.org"), "Opening Coursera..."),
    "eduplus": lambda: (webbrowser.open("https://mauli.edupluscampus.com"), "Opening Edu Plus Login Page..."),
    "universityresult": lambda: (webbrowser.open("https://sgbau.ucanapply.com/"), "You can check the results here..."),
    "sgbau": lambda: (webbrowser.open("https://sgbau.ucanapply.com/"), "Here is the official website of SGBAU..."),

    # Utility Commands
    "weather": lambda: (webbrowser.open("https://www.google.com/search?q=weather"), "Here is the weather update..."),
    "news": lambda: (webbrowser.open("https://news.google.com"), "Here are the latest news updates..."),
    "calculator": lambda: (webbrowser.open("https://www.google.com/search?q=calculator"), "Opening Calculator..."),
    "calendar": lambda: (webbrowser.open("https://calendar.google.com"), "Opening Google Calendar..."),

    #Finance Sites
    "stockmarket": lambda: (webbrowser.open("https://www.marketwatch.com"), "Opening MarketWatch..."),
    "bitcoinprice": lambda: (webbrowser.open("https://www.coindesk.com"), "Opening CoinDesk..."),
    "forbes": lambda: (webbrowser.open("https://www.forbes.com/finance/"), "Opening Forbes Finance..."),
    "financialcalculator": lambda: (webbrowser.open("https://www.bankrate.com/calculators/"), "Opening Bankrate Calculators..."),
    "moneycontrol": lambda: (webbrowser.open("https://www.moneycontrol.com"), "Opening MoneyControl..."),
    "economic times": lambda: (webbrowser.open("https://economictimes.indiatimes.com/markets"), "Opening Economic Times..."),
    "ndtv profit": lambda: (webbrowser.open("https://www.ndtv.com/business"), "Opening NDTV Profit..."),
    "yahoo financeindia": lambda: (webbrowser.open("https://in.finance.yahoo.com"), "Opening Yahoo Finance India..."),
    "financial express": lambda: (webbrowser.open("https://www.financialexpress.com/market"), "Opening Financial Express..."),
    "mint": lambda: (webbrowser.open("https://www.livemint.com"), "Opening Mint..."),


    # Food & Shopping
    "restaurant": lambda: (webbrowser.open("https://google.com/search?q=restaurants near me"), "Searching for restaurants near you..."),
    "onlineshopping": lambda: (webbrowser.open("https://google.com/search?q=online shopping"), "You can shop online from these websites..."),
    "amazon": lambda: (webbrowser.open("https://amazon.com"), "Opening Amazon..."),
    "flipkart": lambda: (webbrowser.open("https://www.flipkart.com"), "Opening Flipkart..."),
    "myntra": lambda: (webbrowser.open("https://www.myntra.com"), "Opening Myntra..."),
    "zomato": lambda: (webbrowser.open("https://www.zomato.com"), "Opening Zomato..."),
    "swiggy": lambda: (webbrowser.open("https://www.swiggy.com"), "Opening Swiggy..."),
    # Travel & Food Sites
    "makemytrip": lambda: (webbrowser.open("https://www.makemytrip.com"), "Opening MakeMyTrip..."),
    "cleartrip": lambda: (webbrowser.open("https://www.cleartrip.com"), "Opening Cleartrip..."),
    "yatra": lambda: (webbrowser.open("https://www.yatra.com"), "Opening Yatra..."),
    "goibibo": lambda: (webbrowser.open("https://www.goibibo.com"), "Opening Goibibo..."),
    "irctc": lambda: (webbrowser.open("https://www.irctc.co.in"), "Opening IRCTC..."),
    "dominos": lambda: (webbrowser.open("https://www.dominos.co.in"), "Opening Domino's India..."),
    "freshmenu": lambda: (webbrowser.open("https://www.freshmenu.com"), "Opening FreshMenu..."),
    "ubereats": lambda: (webbrowser.open("https://www.ubereats.com"), "Opening UberEats..."),

    "currency converter": lambda: (webbrowser.open("https://www.xe.com/currencyconverter/"), "Opening Currency Converter..."),



    "introduce yourself": lambda: ("", "txt\\say.txt"),
    "who are you": lambda: ("", "txt\\say.txt"),

}


# Function to process user queries
def process_query(user_query):
    user_query = user_query.lower().strip()

     # Detect "remind me to ..." pattern
    match = re.search(r"remind me to (.+) in (\d+) (seconds?|minutes?|hours?)", user_query)
    if match:
        task = match.group(1)
        time_value = int(match.group(2))
        unit = match.group(3)

        # Convert time units to seconds
        if "minute" in unit:
            time_value *= 60
        elif "hour" in unit:
            time_value *= 3600

        return setReminder(task, time_value)


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
    if "introduce yourself" in user_query or "who are you" in user_query:
        return read_text_file("say.txt")

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

    if "screenshot" in user_query or "capture screen" in user_query or "take a screenshot" in user_query:
        filename = take_screenshot()
        return f"Screenshot taken and saved"
    
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

    if "what is my ip" in user_query or "show my ip" in user_query or "tell my ip" in user_query:
        ip = get_ip()
        if ip:
            return f"Your current IP address is {ip}."
        else:
            return "Sorry, I couldn't fetch your IP address right now."
    
    if "close tab" in user_query or "close the tab" in user_query or "close current tab" in user_query or "tab close" in user_query or "close this tab" in user_query:
        close_tab()
        return "Closing the current tab."
    
    # Fuzzy match user query with predefined commands
    match, confidence = process.extractOne(user_query, COMMANDS.keys())

    if "pc info" in user_query or "system info" in user_query or "device info" in user_query:
        system_info = get_system_info()
        return system_info

    if confidence > 80:
        response = COMMANDS[match]
        if callable(response):
            _, message = response()
            return message
        return response
    
    # Default action: Google search
    webbrowser.open(f"https://www.google.com/search?q={user_query}")
    return f"Here is what I found for {user_query}"