import wp2.api.creds
import json
import requests

def fetch(api_key, endpoint):
    headers = {
        'Content-Type': 'application/json',
        'x-Auth-App-Key': api_key,
    }

    response = requests.get(wp2.api.creds.url + endpoint, headers=headers)
    response = response.json()
    return response


def get_services(clientId=''):
    return fetch(wp2.api.creds.read_key, 'clients' + clientId + '/services')

def get_clients(clientId=''):
    return fetch(wp2.api.creds.read_key, 'clients' + clientId)

def get_invoices(id='', params=''):
    return fetch(wp2.api.creds.read_key, 'invoices' + id + params)


def update(api_key, endpoint, payload):
    headers = {
        'Content-Type': 'application/json',
        'x-Auth-App-Key': api_key,
    }

    response = requests.patch(wp2.api.creds.url + endpoint, payload, headers=headers)
    print(response)

def update_client(clientId, payload):
    payload = json.dumps(payload)
    payload = str.encode(payload)
    return update(wp2.api.creds.write_key, 'clients/' + clientId, payload)

def create(api_key, endpoint, payload):
    headers = {
        'Content-Type': 'application/json',
        'x-Auth-App-Key': api_key,
    }

    response = requests.post(wp2.api.creds.url + endpoint, payload, headers=headers)
    return response

def create_payment(payload):
    payload = json.dumps(payload)
    payload = str.encode(payload)
    return create(wp2.api.creds.write_key, 'payments', payload)

def create_job(payload):
    payload = json.dumps(payload)
    payload = str.encode(payload)
    response = create(wp2.api.creds.write_key, 'scheduling/jobs', payload)
    print(response)
