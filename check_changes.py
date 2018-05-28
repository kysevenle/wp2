import wp2
import json

def main():
    clients = wp2.api.calls.get_clients_as_dict('id')

    services = wp2.api.calls.get_services()

    connections = {}

    for service in services:
        if service['status'] == 2:
            continue
        connectionId = service['id']
        clientId = service['clientId']
        connections[connectionId] = {
            'IPs': service['ipRanges'],
            'serviceAddress': service['street1'],
            'clientAddress': clients[clientId]['street1'],
        }

    with open(r'C:\Users\Kyle\Dropbox\connections.json', 'r') as old_connection_file:
        old_connections = json.load(old_connection_file)

    if json.dumps(connections) == json.dumps(old_connections):
        print("No Changes Detected")
    else:
        print("Changes have been made. Script will run")
        with open(r'C:\Users\Kyle\Dropbox\connections.json', 'w') as connection_file:
            json.dump(connections, connection_file)
            print("Archive file has been updated")

if __name__ == "__main__":
    main()
