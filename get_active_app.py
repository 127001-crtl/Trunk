'''
Logic:
1: records which app is currently open
2: starts a timer for when the app is open + rounds it to nearest minute 
3: stores data in a json for react app to display values 
'''
import win32gui
import win32process
import psutil
import time 
import json
import os
import win32gui
import win32process
import psutil
import time
import json
import os

def get_foreground_app():
    hwnd = win32gui.GetForegroundWindow()  # Get handle to foreground window
    _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Get process ID
    process = psutil.Process(pid)  # Get process by ID
    return process.name(), win32gui.GetWindowText(hwnd)  # Return app name and window title

file_path = 'data.json'
check = True  # Set to True to start logging, will create it as a global variable to change later!

# Create the file if it doesn't exist, it will be deleted every hour 
if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        json.dump([], f)

while check:
    time.sleep(1)
    app_name, window_title = get_foreground_app()
    print(f"Active App: {app_name} | Window Title: {window_title}") #prints now for saftey feature must delete after!
    
    # Load current data
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Append new entry with timestamp
    data.append({
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'app_name': app_name,
        'window_title': window_title
    })
    
    # Save updated data
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


    #second JSON file!

    with open(file_path, 'r') as f: 
        data = json.load(f) #loads the JSON file to a variable as dictionary to data
    
    
    apps_seen = []

    for entry in data:
        app = entry['app_name']
        if app not in apps_seen:
            apps_seen.append(app)
    
    app_counts = {}  # create dictionary to store counts

    
    for app_name in apps_seen:
        count = sum(1 for entry in data if entry['app_name'] == app_name)
        app_counts[app_name] = count  # store count in dictionary

    # Write all counts once, after the loop
    with open('iterations.json', 'w') as f:
        json.dump(app_counts, f, indent=4)

    if os.path.exists(file_path):
        file_age = time.time() - os.path.getmtime(file_path)
        if file_age > 3600:  # 1 hour = 3600 seconds
            os.remove(file_path)
            print("data.json deleted after 1 hour.")
    
    if os.path.exists('iterations.json'):
        file_age = time.time() - os.path.getmtime('iterations.json')
        if file_age > 86400:  # 24 hours = 86400 seconds
            os.remove('iterations.json')
            print("Deleted iterations.json after 24 hours")
    