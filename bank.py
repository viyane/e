# bank.py

class InsufficientFundsError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

class AccountLockedError(Exception):
    pass


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []
        self.locked = False

    def __str__(self):
        status = "LOCKED" if self.locked else "active"
        return f"{self.owner}'s account — £{self.balance:.2f} ({status})"

    def deposit(self, amount):
        if self.locked:
            raise AccountLockedError("Account is locked")
        if amount <= 0:
            raise InvalidAmountError(f"Deposit amount must be positive: {amount}")
        self.balance += amount
        self.transactions.append(f"Deposit: +£{amount:.2f}")
        return self.balance

    def withdraw(self, amount):
        if self.locked:
            raise AccountLockedError("Account is locked")
        if amount <= 0:
            raise InvalidAmountError(f"Withdrawal amount must be positive: {amount}")
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Cannot withdraw £{amount:.2f} — balance is only £{self.balance:.2f}"
            )
        self.balance -= amount
        self.transactions.append(f"Withdrawal: -£{amount:.2f}")
        return self.balance

    def print_statement(self):
        print(f"\n=== Statement for {self.owner} ===")
        if not self.transactions:
            print("  No transactions yet")
        for t in self.transactions:
            print(f"  {t}")
        print(f"  Balance: £{self.balance:.2f}")


def safe_deposit(account, amount):
    try:
        account.deposit(amount)
        print(f"  Deposited £{amount:.2f} — new balance: £{account.balance:.2f}")
    except InvalidAmountError as e:
        print(f"  Invalid deposit: {e}")
    except AccountLockedError as e:
        print(f"  Account locked: {e}")


def safe_withdraw(account, amount):
    try:
        account.withdraw(amount)
        print(f"  Withdrew £{amount:.2f} — new balance: £{account.balance:.2f}")
    except InsufficientFundsError as e:
        print(f"  Failed: {e}")
    except InvalidAmountError as e:
        print(f"  Invalid withdrawal: {e}")
    except AccountLockedError as e:
        print(f"  Account locked: {e}")


# --- run it ---

acc = BankAccount("Viyan", 100)
print(acc)
print()

print("=== Deposits ===")
safe_deposit(acc, 50)
safe_deposit(acc, -20)
safe_deposit(acc, 200)

print()
print("=== Withdrawals ===")
safe_withdraw(acc, 30)
safe_withdraw(acc, 500)
safe_withdraw(acc, 0)

print()
print("=== Locking account ===")
acc.locked = True
safe_deposit(acc, 100)
safe_withdraw(acc, 50)

acc.print_statement()