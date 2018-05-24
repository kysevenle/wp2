import csv
import wp2
import os
import calendar


def get_clients_as_dict():
    clients_list = wp2.api.calls.get_clients()
    clients = {}
    for client in clients_list:
        id = client['userIdent']
        clients[id] = client
    return clients


def upload_vanco_batches(clients):
    fieldnames = ['vancoId', 'vancoName', 'accountNumber', 'amount', 'datePaid', 'dateDeposited', 'unknown1', 'unknown2', 'referanceNumber', 'firstName', 'middleInitial', 'lastName', 'address', 'unknown3', 'city', 'state', 'zip']
    with os.scandir(r'C:\Users\Kyle\Dropbox\vanco_batches') as files:
        for file in files:
            with open(file.path) as batch:
                reader = csv.DictReader(batch, fieldnames=fieldnames)
                for row in reader:
                    account_number = row['accountNumber']
                    if clients.get(account_number) == None:
                        id = None
                    else:
                        id = clients[account_number]['id']
                    amount = float(row['amount'])
                    payment_time = f"{row['datePaid']}T12:00:00+0000"
                    payload = {
                        'clientId': id,
                        'method': 99,
                        'createdDate': payment_time,
                        'amount': round(amount, 2),
                        'currencyCode': 'USD',
                        'providerName': 'Vanco',
                        'providerPaymentId': row['referanceNumber'],
                        'providerPaymentTime': payment_time,
                        'applyToInvoicesAutomatically': True,
                    }
                    print(payment_time + ' - ' + row['firstName'] + ', ' + row['lastName'])
                    #print(payload)
                    wp2.api.calls.create_payment(payload)
            os.rename(file.path, r"C:\Users\Kyle\Dropbox\Vanco Batches Archive" + '\\' + file.name)


def upload_authorize_batches():
    clients = get_clients_as_dict()
    with os.scandir(r'C:\Users\Kyle\Dropbox\Authorize Batches') as files:
        for file in files:
            with open(file.path) as batch:
                reader = csv.DictReader(batch, delimiter='\t')
                for row in reader:
                    if row['Customer ID'] == '':
                        account_number = row['Phone']
                    else:
                        account_number = row['Customer ID']
                    if clients.get(account_number) == None:
                        id = None
                    else:
                        id = clients[account_number]['id']
                    amount = float(row['Total Amount'])
                    date = row['Submit Date/Time'].split()[0]
                    year = date.split('-')[2]
                    month = date.split('-')[1]
                    month = list(calendar.month_abbr).index(month)
                    day = date.split('-')[0]
                    date = f"{year}-{month}-{day}"
                    print(date)

def main():
    clients = get_clients_as_dict()
    upload_vanco_batches(clients)
