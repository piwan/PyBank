from account import Account
from bank_db_sqlite import create_account, list_accounts, get_account, update_account, delete_account, AccountNotFound, \
    init_db

a1 = Account("Jan", "Kowalski", "ul. Kasztanowa 12, 31-092 Kraków", "1234-1234-1234-1234")

init_db()
create_account(a1)
print(list_accounts())

print(get_account("1234-1234-1234-1234"))

a1.owner_last_name = "Nowak"
a1.balance.amount = 11.00
update_account(a1)
print(get_account("1234-1234-1234-1234"))

delete_account(a1.ban)
try:
    print(get_account("1234-1234-1234-1234"))
except AccountNotFound:
    print("The exception was raised, as expected")

