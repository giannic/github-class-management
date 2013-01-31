from subprocess import check_call

import getpass
import json
import sys

import requests


class GithubException(Exception):
    pass


class Github(object):
    API_URL = "https://api.github.com"

    def __init__(self, token=None):
        self.token = token

    def make_url(self, method):
        return self.API_URL + method

    def get(self, method):
        url = self.make_url(method)

        params = {'per_page': "100"}
        if self.token:
            params['access_token'] = self.token

        req = requests.get(url, params=params)
        if req.status_code not in [200, 201]:
            req.raise_for_status()
        else:
            return req.json()

    def post(self, method, data=None):
        url = self.make_url(method)

        params = {}
        if self.token:
            params['access_token'] = self.token

        req = requests.post(url, params=params, data=data)
        if req.status_code != 201:
            req.raise_for_status()
        else:
            return req.json()


# Adapted from https://github.com/hogbait/6170_repo_management/
def get_auth_token():
    """Get an auth token for use with the API"""
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
        raise GithubException("Error retrieving auth token")
    else:
        return r.json()['token']


def clone_hw_repos(organization):
    """Clone the homework repos for the given organization"""
    g = Github(get_auth_token())

    method = "/orgs/%s/repos" % organization

    for repo in g.get(method):
        if repo['name'].startswith("hw_"):
            print "Cloning %s" % repo['name']
            check_call(["git", "clone", "-b", "master", repo['ssh_url']])
        else:
            print "Skipping %s" % repo['name']


if __name__ == "__main__":
    if sys.argv[1] == "clone":
        clone_hw_repos(sys.argv[2])
    elif sys.argv[1] == "auth":
        print get_auth_token()
