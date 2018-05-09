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


def get_services():
    return fetch(wp2.api.creds.read_key, 'clients/services')

def get_clients():
    return fetch(wp2.api.creds.read_key, 'clients')

def get_clients_services(client_id):
    return fetch(wp2.api.creds.read_key, 'clients/' + client_id + '/services')
