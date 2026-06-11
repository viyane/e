# test_bank.py

import pytest
from bank import BankAccount, InsufficientFundsError, InvalidAmountError, AccountLockedError


@pytest.fixture
def account():
    return BankAccount("Viyan", 100)


@pytest.fixture
def empty_account():
    return BankAccount("Alice", 0)


@pytest.fixture
def locked_account():
    acc = BankAccount("Bob", 500)
    acc.locked = True
    return acc


# --- deposit tests ---

def test_deposit_increases_balance(account):
    account.deposit(50)
    assert account.balance == 150

def test_deposit_returns_new_balance(account):
    result = account.deposit(50)
    assert result == 150

def test_deposit_zero_raises(account):
    with pytest.raises(InvalidAmountError):
        account.deposit(0)

def test_deposit_negative_raises(account):
    with pytest.raises(InvalidAmountError):
        account.deposit(-10)

def test_deposit_locked_raises(locked_account):
    with pytest.raises(AccountLockedError):
        locked_account.deposit(50)


# --- withdraw tests ---

def test_withdraw_decreases_balance(account):
    account.withdraw(30)
    assert account.balance == 70

def test_withdraw_full_balance(account):
    account.withdraw(100)
    assert account.balance == 0

def test_withdraw_too_much_raises(account):
    with pytest.raises(InsufficientFundsError):
        account.withdraw(200)

def test_withdraw_zero_raises(account):
    with pytest.raises(InvalidAmountError):
        account.withdraw(0)

def test_withdraw_negative_raises(account):
    with pytest.raises(InvalidAmountError):
        account.withdraw(-10)

def test_withdraw_locked_raises(locked_account):
    with pytest.raises(AccountLockedError):
        locked_account.withdraw(50)

def test_withdraw_from_empty_raises(empty_account):
    with pytest.raises(InsufficientFundsError):
        empty_account.withdraw(1)


# --- transaction log tests ---

def test_deposit_recorded_in_transactions(account):
    account.deposit(50)
    assert len(account.transactions) == 1

def test_withdraw_recorded_in_transactions(account):
    account.withdraw(30)
    assert len(account.transactions) == 1

def test_failed_withdraw_not_recorded(account):
    try:
        account.withdraw(500)
    except InsufficientFundsError:
        pass
    assert len(account.transactions) == 0

def test_multiple_transactions(account):
    account.deposit(50)
    account.withdraw(20)
    assert len(account.transactions) == 2


# --- account state tests ---

def test_initial_balance(account):
    assert account.balance == 100

def test_initial_owner(account):
    assert account.owner == "Viyan"

def test_initial_not_locked(account):
    assert account.locked == False

def test_str_shows_owner(account):
    assert "Viyan" in str(account)

def test_str_shows_balance(account):
    assert "100" in str(account)
