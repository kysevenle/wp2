import wp2
import json

clients = wp2.api.calls.get_clients_as_dict('id')

services = wp2.api.calls.get_services()

connections = {}

for service in services:
    connectionId = service['id']
    clientId = service['clientId']
    connections[connectionId] = {
        'IPs': service['ipRanges'],
        'serviceAddress': service['street1'],
        'clientAddress': clients[clientId]['street1'],
    }
