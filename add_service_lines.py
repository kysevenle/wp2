import csv
import re
import work_package2


#Create a List of Dicts containing Mac and Port
def get_switch_arp(switch_arp):
    with open(switch_arp) as file:
        reader = csv.reader(file, skipinitialspace=True)
        header = next(reader)
        connects = [dict(zip(header, row)) for row in reader]
        #convert mac format from xx.xx.xx.xx.xx.xx to xxxx.xxxx.xxxx
        for connect in connects:
            connect = connect.upper()
            if re.fullmatch('\w\w\w\w.\w\w\w\w.\w\w\w\w'):
                continue
            elif re.fullmatch('\w\w-\w\w-\w\w-\w\w-\w\w-\w\w', connect['Mac_Address']):
                connect['Mac_Address'] = connect['Mac_Address'][0:2] + connect['Mac_Address'][3:5] + '.' + connect['Mac_Address'][6:8] + connect['Mac_Address'][9:11] + '.' + connect['Mac_Address'][12:14] + connect['Mac_Address'][15:17]
            elif re.fullmatch('\w\w\w\w\w\w\w\w\w\w\w\w', connect['Mac_Address']):
                connect['Mac_Address'] = connect['Mac_Address'][0:2] + connect['Mac_Address'][2:4] + '.' + connect['Mac_Address'][4:6] + connect['Mac_Address'][6:8] + '.' + connect['Mac_Address'][8:10] + connect['Mac_Address'][10:12]
        return connects

#Add IPs to connects
def add_ips(connects):
    with open(r'c:\Users\Kyle\Desktop\master_arp.csv') as file:
            arp_reader = csv.DictReader(file)
            for line in arp_reader:
                for connect in connects:
                    if connect['Mac_Address'] == line['MAC ADDRESS']:
                        connect['IP'] = line['IP Address']
            for connect in connects:
                if 'IP' not in connect:
                    connect['IP'] = input(connect['Mac_Address'] + ' - Not Found, Enter IP - ')

def add_line_names(connects):
    ports = set()
    for connect in connects:
        ports.add(connect['Port'])
    lines = []
    for port in ports:
        lines.append({'Port':port, 'Line_Name': input('Name of line for port - ' + port + ' - ')})
    for connect in connects:
        for line in lines:
            if connect['Port'] == line['Port']:
                connect['Line'] = line['Line_Name']

def main():

    switch_arp = input('Enter Csv filename for switch arp - ')

    #Create List of Dicts containing Mac and Port
    connects = get_switch_arp(switch_arp)

    #Add IPs to connects
    add_ips(connects)

    #Add line names to connects
    add_line_names(connects)

    services = work_package2.api.calls.get_services()

    for service in services:
        for connect in connects:
            if connect['Line'] == 'Ignore':
                continue
            elif service['status'] == 2:
                continue
            elif connect['IP'] in service['ipRanges']:
                print(str(service['clientId']) + ' - ' + connect['Line'])

if __name__ == '__main__':
    main()
