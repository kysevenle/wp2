import wp2
import datetime


def main():
    wp2.upload_payments.main()
    wp2.maintain.late_fee_check()
    wp2.maintain.credit_balance_check()

if __name__ == '__main__':
    main()
