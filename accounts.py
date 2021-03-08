from enum import Enum, auto


class AccountType(Enum):
    Asset = auto()
    Liability = auto()
    Equity = auto()
    Income = auto()
    Expense = auto()
