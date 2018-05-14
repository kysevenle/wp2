import wp2.api.creds
from urllib.request import urlopen, Request
import json

def fetch(api_key, endpoint):
    headers = {
        'Content-Type': 'application/json',
        'x-Auth-App-Key': api_key,
    }

    request = Request(wp2.api.creds.url + endpoint, headers=headers)

    response_body = urlopen(request).read()
    json_obj = response_body

    data = json.loads(json_obj)

    return data


def get_services(clientId=''):
    return fetch(wp2.api.creds.read_key, 'clients' + clientId + '/services')

def get_clients(clientId=''):
    return fetch(wp2.api.creds.read_key, 'clients' + clientId)
