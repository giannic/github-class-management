# Adapted from https://github.com/hogbait/6170_repo_management/blob/master/run.py
import getpass
import json

import requests


print "Enter your Github credentials"
username = raw_input("Username: ")
password = getpass.getpass("Password: ")
url = "https://api.github.com/authorizations"
data = {
    'scopes': ['gist', 'delete_repo', 'repo:status',
               'repo', 'public_repo', 'user'],
    'note': 'GitHomework',
}

r = requests.post(url, data=json.dumps(data), auth=(username, password))
if r.status_code != 201:
    print "Error retrieving auth token"
else:
    print r.json()['token']
