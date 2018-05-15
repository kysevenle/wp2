import wp2
import re
import datetime

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

def get_days_overdue():
    invoices = wp2.api.calls.get_invoices('?overdue=1')
    today = datetime.date.today()
    for invoice in invoices:
        due_date = invoice['dueDate'].split('T')
        due_date = due_date[0]
        year, month, day = due_date.split('-')
        due_date = datetime.date(int(year), int(month), int(day))
        days_overdue = today - due_date
        print(str(days_overdue))
