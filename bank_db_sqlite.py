import sqlite3

from account import Account
from money import Monetary

db_file = "bank.db"


def init_db():
    """Initialize Bank database"""
    conn = sqlite3.connect(db_file)
    conn.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (owner_first_name text, owner_last_name text, owner_address text, 
                 ban text, balance_amount real, balance_currency text)''')
    conn.commit()
    conn.close()


def create_account(account):
    """
    CRUD create
    :param account: Account to be created
    :return: None
    """
    conn = sqlite3.connect(db_file)
    conn.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)",
                 (account.owner_first_name, account.owner_last_name, account.owner_address,
                  account.ban, account.balance.amount, account.balance.currency))
    conn.commit()
    conn.close()


def list_accounts():
    """
    :return: list of Account objects
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    result = []
    for row in cursor.fetchall():
        result.append(Account(row[0], row[1], row[2], row[3], Monetary(row[4], row[5])))
    conn.close()

    return result


def get_account(ban):
    """
    :param ban: Account.ban (Bank Account Number)
    :return: Account object
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE ban=?", (ban,))
    row = cursor.fetchone()
    if row:
        result = Account(row[0], row[1], row[2], row[3], Monetary(row[4], row[5]))
    else:
        raise AccountNotFound(ban)
    conn.close()

    return result


def update_account(account):
    """
    :param account: Account object to be updated
    :return: None
    """
    conn = sqlite3.connect(db_file)
    conn.execute("UPDATE accounts "
                 "SET owner_first_name=?, owner_last_name=?, owner_address=?, "
                 "balance_amount=?, balance_currency=? "
                 "WHERE ban=?",
                 (account.owner_first_name, account.owner_last_name, account.owner_address,
                  account.balance.amount, account.balance.currency, account.ban))
    conn.commit()
    conn.close()


def delete_account(ban):
    """
    :param ban: Bank Account Number
    :return: None
    """
    conn = sqlite3.connect(db_file)
    conn.execute("DELETE FROM accounts WHERE ban=?", (ban,))
    conn.commit()
    conn.close()


def transfer_money(from_account, to_account, amount):
    """
    :param from_account: Account
    :param to_account: Account
    :param amount: Monetary units
    :return: None
    """
    conn = sqlite3.connect(db_file)

    # TODO: fetch accounts from the database, to make sure we're working on the latest entities

    # validate
    if from_account.balance < amount:
        raise TransactionNotAllowed(from_account.ban, to_account.ban, "insufficient funds")

    # perform transaction
    from_account.balance = from_account.balance - amount
    to_account.balance = to_account.balance + amount
    update_account(from_account)
    update_account(to_account)

    conn.commit()
    conn.close()


class AccountNotFound(Exception):
    """Exception raised when BAN was not found in the DB"""

    def __init__(self, ban):
        super().__init__("Account {} not found".format(ban))


class TransactionNotAllowed(Exception):
    """Exception raised when transaction cannot be performed because of e.g. insufficient funds"""

    def __init__(self, ban_1, ban_2, reason):
        super().__init__("Transaction between {} and {} couldn't be done because of {}".format(ban_1, ban_2, reason))
