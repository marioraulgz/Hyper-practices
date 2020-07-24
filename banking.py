# Write your code here
import random
import sqlite3

bank_db = dict()

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute(
    'CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()


def luhn(number_without_checksum):
    total = 0
    for i, number in enumerate(number_without_checksum, start=1):
        number = int(number)
        if i % 2 != 0:
            number *= 2
        if number > 9:
            number -= 9
        total += number
    if (total % 10) != 0:
        return abs((total % 10) - 10)
    else:
        return 0


def check_luhn(card_number):
    without_checksum = card_number[:-1]
    checksum = str(luhn(without_checksum))
    correct_card_number = without_checksum + checksum
    if correct_card_number == card_number:
        return True
    else:
        return False


def create_account():
    account_identifier = str(400000)
    bin = str(random.randint(100000000, 999999999))
    checksum = str(luhn(account_identifier + bin))
    card_number = account_identifier + bin + checksum
    card_pin = str(random.randint(1000, 9999))
    bank_db[card_number] = card_pin

    cur.execute('INSERT INTO card (number, pin) VALUES (?, ?)', (card_number, card_pin))
    conn.commit()

    print("Your card has been created\nYour card number:\n{}".format(card_number))
    print("Your card PIN:\n{}".format(card_pin))
    print()


def home_screen():
    print("""1. Create an account
2. Log into account
0. Exit""")


def home_screen_logged():
    print("""1. Balance
2. Add income
3. Do transfer
4. Log out
0. Exit""")


def log_into_account():
    card_input = input("Enter your card number:\n")
    pin_input = input("Enter your PIN:\n")

    cur.execute('SELECT * FROM card WHERE number = ? and pin = ?', (card_input, pin_input))
    account = cur.fetchone()
    if account is None:
        print("\nWrong card number or PIN!\n")
    else:
        print("\nYou have successfully logged in!\n")
        atm_logged(account)


def get_balance(account):
    acccount_info(account)
    print('Balance: {}\n'.format(account[3]))


def add_income(account):
    quantity = input("\nEnter income:\n")
    cur.execute('UPDATE card SET balance = balance + ? WHERE number = ? ', (quantity, account[1]))
    conn.commit()
    print('Income was added!\n')


def close_account(account):
    cur.execute('DELETE FROM card WHERE number = ?', (account[1],))
    conn.commit()
    print('\nThe account has been closed!\n')


def check_membership(card):
    cur.execute('SELECT * FROM card WHERE number = ? ', (card,))
    return cur.fetchone()


def acccount_info(account):
    cur.execute('SELECT * FROM card WHERE number = ? and pin = ?', (account[1], account[2]))
    return cur.fetchone()


def transfer(account):
    refreshed_account = acccount_info(account)
    receiving_card = input('\nEnter card number:\n')
    if check_luhn(receiving_card):
        if check_membership(receiving_card) is None:
            print('Such a card does not exist.\n')
        else:
            quantity = int(input('Enter how much money you want to transfer:\n'))
            if quantity <= int(refreshed_account[3]):
                cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (quantity, receiving_card))
                cur.execute('UPDATE card SET balance = balance - ? WHERE number = ?', (quantity, refreshed_account[1]))
                conn.commit()
                print('Success!\n')
            else:
                print('Not enough money!\n')
    else:
        print('Probably you made mistake in the card number.\nPlease try again!\n')


def atm_logged(account):
    while True:
        home_screen_logged()
        choice_logged = int(input())
        if choice_logged == 1:
            get_balance(account)
        elif choice_logged == 2:
            add_income(account)
        elif choice_logged == 3:
            transfer(account)
        elif choice_logged == 4:
            close_account(account)
        elif choice_logged == 5:
            print("\nYou have successfully logged out!\n")
            break
        elif choice_logged == 0:
            print("\nBye!")
            exit()


def atm():
    while True:
        home_screen()
        choice = int(input())
        print()

        if choice == 1:
            create_account()
        elif choice == 2:
            log_into_account()
        elif choice == 0:
            print("\nBye!")
            break


atm()
