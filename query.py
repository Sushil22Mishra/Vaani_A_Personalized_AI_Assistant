import datetime
import webbrowser
import pyautogui
import requests
import time


#function for opening apps
def openApp(appName):
    
    pyautogui.press('win')
    pyautogui.typewrite(appName)
    
    pyautogui.press('=')
    pyautogui.press('enter')

    
# Define a function for processing queries
def process_query(user_query):
   
    response = ''
    user_query = user_query.lower()
    if 'hello' in user_query:
        response = 'Hi.  I am Vaani What can i help you with ?'
    #App Launching
    elif 'launch' in user_query:
            appName=  user_query.split('launch')[1]
            openApp(appName) 
            response = (f'Opening {appName}')  
       
    # elif 'what is Vaani' in user_query:
    #     with open("txt\say.txt", 'r') as file:
    #         content = file.read()
    #         response = content

    # elif 'how do you work' in user_query:
    #     with open("txt\work.txt", 'r') as file:
    #         content = file.read()
    #         response = content
    #misc
    elif 'search ' in user_query:
        search_term = user_query.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        response = 'Here is what I found for ' + search_term
        webbrowser.get().open(url)    
    elif 'wikipedia for' in user_query:
        response = 'Searching Wikipedia...'
        search_term = user_query.split("for")[-1]
        url = f"https://en.wikipedia.org/wiki/{search_term}"
        response += ' Here is what I found on wikipedia for ' + search_term
        webbrowser.get().open(url)
    elif 'google drive' in user_query:
            webbrowser.open("https://drive.google.com/drive/my-drive")
            response = 'Opening Google Drive'


    elif 'where is' in user_query:
        location = user_query.split("is")[-1]
        location = location.strip()
        response= (f'here is {location} on Google Maps')
        url = f"https://www.google.com/maps/search/{location}"
        webbrowser.open(url)


    elif 'time ' in user_query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f'the time is : {strTime}')
        response = (f'the time is : {strTime}')

    #educational
    elif 'university result' in user_query or 'sgbau' in user_query:
        webbrowser.open("https://sgbau.ucanapply.com/")
        response = 'You can check the results here '
    elif 'github' in user_query:
            webbrowser.open("https://github.com/")
            response = 'Opening Git Hub'
    elif 'linkedin' in user_query:
            webbrowser.open("https://www.linkedin.com/")
            response = 'Opening LinkedIn' 
    elif 'edu plus' in user_query:
        webbrowser.open("https://mauli.edupluscampus.com/")
        response = 'Opening Edu plus Login Page' 
    elif 'stack overflow' in user_query or 'help in programming' in user_query:
        webbrowser.open("https://stackoverflow.com")
        response = 'Opening Stack Overflow'






    #social media
    elif 'youtube' in user_query:
        webbrowser.open("https://youtube.com")
        response = 'Opening YouTube'
    elif 'instagram' in user_query:
        webbrowser.open("https://instagram.com")
        response = 'Opening Instagram' 
    elif 'facebook' in user_query:
        webbrowser.open("https://facebook.com")
        response = 'Opening Facebook'
    elif 'google' in user_query:
            webbrowser.open("https://google.com")
            response = 'Opening google'
    elif 'twitter' in user_query:
        webbrowser.open("https://twitter.com")
        response = 'Opening Twitter'
    elif 'reddit' in user_query:
        webbrowser.open("https://reddit.com")
        response = 'Opening Reddit'
    elif 'pinterest' in user_query:
        webbrowser.open("https://pinterest.com")
        response = 'Opening Pinterest'
    elif 'gmail' in user_query:
        webbrowser.open("https://gmail.com")
        response = 'Opening Gmail'
    elif 'discord' in user_query:
        webbrowser.open("https://discord.com")
        response = 'Opening Discord'
    elif 'netflix' in user_query:
        webbrowser.open("https://netflix.com")
        response = 'Opening Netflix'
    elif 'whatsapp' in user_query:
            webbrowser.open("https://whatsapp.com")
            response = 'Opening WhatsApp'
    elif 'amazon' in user_query:
            webbrowser.open("https://amazon.com")
            response = 'Opening Amazon you can shop online here'

    elif 'online shopping' in user_query or 'shop online' in user_query or 'e-commerce' in user_query:
                url = f"https://google.com/search?q=online shopping"
                response = 'You can shop online from these Websites '
                webbrowser.get().open(url)
    
    elif 'restaurant' in user_query or 'restaurants'in user_query:
                url = f"https://google.com/search?q=restaurants near me "
                response = 'These are some well known places near you'
                webbrowser.get().open(url)
    #if no data to show
    else:
        search_term = user_query
        url = f"https://google.com/search?q={search_term}"
        response = 'Here is what I found for ' + search_term
        webbrowser.get().open(url)

   
        
    return response