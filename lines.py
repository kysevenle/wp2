import wp2

def main():
    devices = wp2.api.calls.get_devices()

    interfaces = {}

    for device in devices:
        device_ints = wp2.api.calls.get_device_ints(str(device['id']))
        for interface in device_ints:
            id = interface['id']
            interfaces[id] = interface
            interfaces[id]['deviceName'] = device['name']
            interfaces[id]['clientIps'] = []

    services = wp2.api.calls.get_services()

    no_interface = []

    for service in services:
        service_devices = wp2.api.calls.get_service_devices(str(service['id']))
        for service_device in service_devices:
            interface_id = service_device['interfaceId']
            print(str(interface_id) + '----' + str(service_device['id']))
            if interfaces.get(interface_id) == None:
                no_interface.append(service['clientId'])
            else:
                for ip in service['ipRanges']:
                    interfaces[interface_id]['clientIps'].append(ip)

    for interface, interface_info in interfaces.items():
        if not interface_info['clientIps']:
            continue
        else:
            with open(r'C:/Users/Kyle/Desktop/lines/' + interface_info['deviceName'] + '_' + interface_info['name'] + '.txt', 'w') as file:
                for ip in interface_info['clientIps']:
                    file.write(ip + '\n')


if __name__ == "__main__":
    main()
