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
        if days_overdue == datetime.timedelta(days=16):
            print(invoice['clientId'])

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
