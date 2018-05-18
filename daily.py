import wp2
import datetime

def late_fee_check():
    invoices = wp2.api.calls.get_invoices('?overdue=1')
    today = datetime.date.today()
    for invoice in invoices:
        due_date = invoice['dueDate'].split('T')
        due_date = due_date[0]
        year, month, day = due_date.split('-')
        due_date = datetime.date(int(year), int(month), int(day))
        days_overdue = today - due_date
        if days_overdue == datetime.timedelta(days=16) and invoice['total'] - invoice['amountPaid'] <= 15:
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
            if round(client['accountBalance']) == round(client['accountCredit']):
                continue
            else:
                payload = {
                    'title': 'Apply credit to invoices',
                    'description': "Apply account's credit to account's invoices",
                    'clientId': client['id'],
                }
                wp2.api.calls.create_job(payload)

def main():
    late_fee_check()
    credit_balance_check()

if __name__ == '__main__':
    main()
