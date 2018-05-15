import wp2
import re

def check_for_service_notes_by_area(area_regex):
    services = wp2.api.calls.get_services()
    for service in services:
        for ip in service['ipRanges']:
            if re.match(area_regex, ip):
                print(ip, service['note'])

def late_fee_check():
    invoices = wp2.api.calls.get_invoices('?overdue=1')
    for invoice in invoices:
        if invoice['total'] - invoice['amountPaid'] < 15:
            print(invoice['clientId'])
