import wp2

devices = wp2.api.calls.get_devices()

interfaces = {}

for device in devices:
    device_ints = wp2.api.calls.get_device_ints(str(device['id']))
    for interface in device_ints:
        id = interface['id']
        interfaces[id] = interface
        interfaces[id]['clientIps'] = []

services = wp2.api.calls.get_services()

no_interface = []

for service in services:
    if service['status'] == 2:
        continue
    else:
        service_devices = wp2.api.calls.get_service_devices(str(service['id']))
        for service_device in service_devices:
            interface_id = service_device['interfaceId']
            print(str(interface_id) + '----' + str(service_device['id']))
            if interfaces.get(interface_id) == None:
                no_interface.append(service['clientId'])
            else:
                for ip in service['ipRanges']:
                    interfaces[interface_id]['clientIps'].append(ip)
