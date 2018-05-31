import csv
import wp2
import os
import calendar
import logging


logging.basicConfig(
    filename=r'C:\Users\Kyle\Dropbox\payments.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def auth_d_to_ucrm_d(auth_d):
    date = auth_d.split()[0]
    year = date.split('-')[2]
    month = date.split('-')[1]
    month = list(calendar.month_abbr).index(month)
    day = date.split('-')[0]
    if auth_d.split()[2] == 'PM':
        time = auth_d.split()[1]
        if int(time.split(':')[0]) == 12:
            hour = int(time.split(':')[0])
        else:
            hour = int(time.split(':')[0]) + 12
        minute = time.split(':')[1]
        second = time.split(':')[2]
        time = f"{hour}:{minute}:{second}"
    else:
        time = auth_d.split()[1]
        if int(time.split(':')[0]) == 12:
            hour = int(time.split(':')[0]) - 12
        else:
            hour = int(time.split(':')[0])
        hour = time.split(':')[0]
        minute = time.split(':')[1]
        second = time.split(':')[2]
        time = f"{hour}:{minute}:{second}"
    date = f"{year}-{month}-{day}T{time}-0600"
    return date


def upload_vanco_batches(clients):
    fieldnames = ['vancoId', 'vancoName', 'accountNumber', 'amount', 'datePaid', 'dateDeposited', 'unknown1', 'unknown2', 'referanceNumber', 'firstName', 'middleInitial', 'lastName', 'address', 'unknown3', 'city', 'state', 'zip']
    with os.scandir(r'C:\Users\Kyle\Dropbox\vanco_batches') as files:
        for file in files:
            logging.info(f"Uploading payments from {file}")
            with open(file.path) as batch:
                reader = csv.DictReader(batch, fieldnames=fieldnames)
                for row in reader:
                    account_number = row['accountNumber']
                    if clients.get(account_number) == None:
                        id = None
                    else:
                        id = clients[account_number]['id']
                    amount = float(row['amount'])
                    payment_time = f"{row['datePaid']}T13:00:00-0600"
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
                    response = wp2.api.calls.create_payment(payload)
                    print(response)
                    logging.info(f"{response} - {row['referanceNumber']} - {row['firstName']} - {row['lastName']}")
            logging.info(f"Finished uploading payments for {file}")
            os.rename(file.path, r"C:\Users\Kyle\Dropbox\Vanco Batches Archive" + '\\' + file.name)


def upload_authorize_batches(clients):
    with os.scandir(r'C:\Users\Kyle\Dropbox\Authorize Batches') as files:
        for file in files:
            logging.info(f"Uploading payments from {file}")
            with open(file.path, encoding='utf-8-sig') as batch:
                reader = csv.DictReader(batch, delimiter='\t')
                for row in reader:
                    print(row)
                    if row['Response Code'] != '1':
                        continue
                    if row['Customer ID'] == '':
                        account_number = row['Phone']
                    else:
                        account_number = row['Customer ID']
                    if clients.get(account_number) == None:
                        id = None
                    else:
                        id = clients[account_number]['id']
                    amount = float(row['Total Amount'])
                    date = auth_d_to_ucrm_d(row['Submit Date/Time'])
                    payload = {
                        'clientId': id,
                        'method': 9,
                        'createdDate': date,
                        'amount': round(amount, 2),
                        'currencyCode': 'USD',
                        'note': 'Authorize.net Transaction - ' + row['Transaction ID'],
                        'applyToInvoicesAutomatically': True,
                    }
                    print(row['Transaction ID'] + ' - ' + row['Customer First Name'] + ', ' + row['Customer Last Name'])
                    response = wp2.api.calls.create_payment(payload)
                    print(response)
                    logging.info(f"{response} - {row['Transaction ID']} - {row['Customer First Name']} - {row['Customer Last Name']}")
            logging.info(f"Finished uploading payments for {file}")
            os.rename(file.path, r"C:\Users\Kyle\Dropbox\Authorize Batches Archive" + '\\' + file.name)

def main():
    clients = wp2.api.calls.get_clients_as_dict(key='userIdent')
    upload_vanco_batches(clients)
    upload_authorize_batches(clients)

if __name__ == "__main__":
    main()
