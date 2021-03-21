from enum import Enum, auto
from typing import List, Optional, Union

AccountOrRollupList = List[Union["Account", "AccountRollup"]]


class AccountType(Enum):
    Asset = auto()
    Liability = auto()
    Equity = auto()
    Income = auto()
    Expense = auto()
    Unknown = auto()


class AmountType(Enum):
    Debit = auto()
    Credit = auto()


class Account:
    def __init__(
        self, acc_id: str, acc_name: str, acc_type: AccountType = AccountType.Unknown
    ):
        self.name = acc_name
        self.type = acc_type

    def __repr__(self):
        return f'Account "{self.name}" ({self.type})'


class AccountRollup:
    def __init__(self, accounts: AccountOrRollupList = []):
        self.children_accounts: AccountOrRollupList = accounts

    def __repr__(self):
        return str(self.children_accounts)


class JournalEntryLeg:
    def __init__(self, account: Account, amount: float, amount_type: AmountType):
        self.account = account
        self.amount = abs(amount)
        self.amount_type = amount_type

    @property
    def signed_amount(self):
        return self.amount if self.amount_type == AmountType.Debit else -self.amount

    def __repr__(self):
        return f"{self.account} ({self.signed_amount} {self.amount_type})"


class JournalEntry:
    def __init__(self, journal_legs: Optional[List[JournalEntryLeg]]):
        self.journal_legs: List[JournalEntryLeg] = journal_legs

    def is_balanced(self) -> bool:
        return sum(self._signed_amounts) == 0

    @property
    def _signed_amounts(self) -> List[float]:
        return [leg.signed_amount for leg in self.journal_legs]

    def __repr__(self):
        return str(self.journal_legs)


# Setup chart of accounts
cash_account = Account(1, "Cash", AccountType.Asset)
mortgage_account = Account(2, "Mortgage", AccountType.Liability)
revenue_account = Account(3, "Revenues", AccountType.Income)

balance_sheet = AccountRollup([cash_account, mortgage_account])

income_statement = AccountRollup(revenue_account)
chart_of_accounts = AccountRollup([balance_sheet, income_statement])

jnl = JournalEntry(
    [
        JournalEntryLeg(cash_account, 100, AmountType.Debit),
        JournalEntryLeg(mortgage_account, 100, AmountType.Credit),
    ]
)
print(jnl)
