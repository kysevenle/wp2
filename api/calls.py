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

def get_services_as_dict():
    services_list = wp2.api.calls.get_services()
    services = {}
    for service in services:
        id = service['id']
        service[id] = service
    return services

def get_clients(clientId=''):
    return fetch(wp2.api.creds.read_key, 'clients' + clientId)

def get_clients_as_dict(key='id'):
    clients_list = wp2.api.calls.get_clients()
    clients = {}
    for client in clients_list:
        id = client[key]
        clients[id] = client
    return clients

def get_invoices(id='', params=''):
    return fetch(wp2.api.creds.read_key, 'invoices' + id + params)

def get_devices():
    return fetch(wp2.api.creds.read_key, 'devices')

def get_service_devices(serviceId):
    return fetch(wp2.api.creds.read_key, 'clients/services/' + serviceId + '/service-devices')

def get_device_ints(device_id):
    return fetch(wp2.api.creds.read_key, 'devices/' + device_id + '/device-interfaces')


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

def update_service_device(service_device_id, payload):
    payload = json.dumps(payload)
    payload = str.encode(payload)
    response = update(wp2.api.creds.write_key, 'clients/services/service-devices/' + service_device_id, payload)
    return(response)

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
    response = create(wp2.api.creds.write_key, 'payments', payload)
    return(response)

def create_job(payload):
    payload = json.dumps(payload)
    payload = str.encode(payload)
    response = create(wp2.api.creds.write_key, 'scheduling/jobs', payload)
    print(response)
