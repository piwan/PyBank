from account import Account
from bank_db_sqlite import create_account, list_accounts, get_account, update_account, delete_account, AccountNotFound, \
    init_db, transfer_money
from money import Monetary

a1 = Account("Jan", "Kowalski", "ul. Kasztanowa 12, 31-092 Kraków", "1234-1234-1234-1234")
a2 = Account("Adam", "Kowalski", "ul. Opolska 100, 31-201 Kraków", "1234-5678-9012-3456")

init_db()
create_account(a1)
create_account(a2)
print(list_accounts())

print(get_account("1234-1234-1234-1234"))

a1.owner_last_name = "Nowak"
a1.balance.amount = 11.00
update_account(a1)
print(get_account("1234-1234-1234-1234"))

# test transfer
transfer_money(a1, a2, Monetary(1, "PLN"))
assert a1.balance.amount == 10.00
assert a2.balance.amount == 1.00

delete_account(a1.ban)
delete_account(a2.ban)
try:
    print(get_account("1234-1234-1234-1234"))
except AccountNotFound:
    print("The exception was raised, as expected")
