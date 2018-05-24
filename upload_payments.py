import csv
import wp2
import os


def upload_vanco_batches():
    fieldnames = ['vancoId', 'vancoName', 'accountNumber', 'amount', 'datePaid', 'dateDeposited', 'unknown1', 'unknown2', 'referanceNumber', 'firstName', 'middleInitial', 'lastName', 'address', 'unknown3', 'city', 'state', 'zip']
    clients_list = wp2.api.calls.get_clients()
    clients = {}
    for client in clients_list:
        id = client['userIdent']
        clients[id] = client
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
