import wp2
import re
import datetime
import json

def check_for_service_notes_by_area(area_regex):
    services = wp2.api.calls.get_services()
    for service in services:
        for ip in service['ipRanges']:
            if re.match(area_regex, ip):
                print(ip, service['note'])

def get_late_fees():
    invoices = wp2.api.calls.get_invoices('?overdue=1')
    today = datetime.date.today()
    for invoice in invoices:
        due_date = invoice['dueDate'].split('T')
        due_date = due_date[0]
        year, month, day = due_date.split('-')
        due_date = datetime.date(int(year), int(month), int(day))
        days_overdue = today - due_date
        if days_overdue == datetime.timedelta(days=15):
            print(invoice['clientId'])

def late_fee_check(days_late=14):
    invoices = wp2.api.calls.get_invoices('?overdue=1')
    today = datetime.date.today()
    for invoice in invoices:
        due_date = invoice['dueDate'].split('T')
        due_date = due_date[0]
        year, month, day = due_date.split('-')
        due_date = datetime.date(int(year), int(month), int(day))
        days_overdue = today - due_date
        if days_overdue == datetime.timedelta(days_late) and invoice['total'] - invoice['amountPaid'] <= 15:
            payload = {
                'title': 'Remove late fee',
                'description': 'Remove late fee from account before invoices are processed',
                'clientId': invoice['clientId'],
            }
            wp2.api.calls.create_job(payload)

def credit_balance_check():
    clients = wp2.api.calls.get_clients()
    for client in clients:
        if client['accountOutstanding'] != 0 and client['accountCredit'] != 0:
            if round(client['accountBalance'], 2) == round(client['accountCredit'], 2):
                continue
            else:
                payload = {
                    'title': 'Apply credit to invoices',
                    'description': "Apply account's credit to account's invoices",
                    'clientId': client['id'],
                }
                wp2.api.calls.create_job(payload)

def remove_signal_stats():
    services = wp2.api.calls.get_services()
    for service in services:
        if service['status'] == 2:
            continue
        else:
            service_devices = wp2.api.calls.get_service_devices(str(service['id']))
            for service_device in service_devices:
                if service_device['createSignalStatistics'] == False:
                    continue
                else:
                    id = str(service_device['id'])
                    payload = {'createSignalStatistics': False}
                    response = wp2.api.calls.update_service_device(id, payload)

def remove_ping_stats():
    services = wp2.api.calls.get_services()
    for service in services:
        if service['status'] == 2:
            continue
        else:
            service_devices = wp2.api.calls.get_service_devices(str(service['id']))
            for service_device in service_devices:
                if service_device['createPingStatistics'] == False:
                    continue
                else:
                    id = str(service_device['id'])
                    print(json.dumps(service, indent=4))
                    payload = {'createPingStatistics': False}
                    response = wp2.api.calls.update_service_device(id, payload)

def find_empty_locations():
    services = wp2.api.calls.get_services()
    for service in services:
        if service['addressGpsLat'] == None:
            payload = {
                'title': 'Resolve GPS',
                'description': "Client has service with no gps location. Resolve GPS",
                'clientId': service['clientId'],
            }
            wp2.api.calls.create_job(payload)
            print(service['clientId'])
