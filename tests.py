from accounts import Account 
from accounts import AccountRollup
from accounts import AccountType
from accounts import AmountType
from accounts import JournalEntry
from accounts import JournalEntryLeg

# Setup chart of accounts
cash_account = Account(1, "Cash", AccountType.Asset)
mortgage_account = Account(2, "Mortgage", AccountType.Liability)
revenue_account = Account(3, "Revenues", AccountType.Income)

balance_sheet = AccountRollup([cash_account, mortgage_account])

income_statement = AccountRollup(revenue_account)
chart_of_accounts = AccountRollup([balance_sheet, income_statement])


def test_journal_entry_balance():
    # Journal entry is balanced if Debit == Credit
    jnl = JournalEntry(
        [
            JournalEntryLeg(cash_account, 50, AmountType.Debit),
            JournalEntryLeg(cash_account, 50, AmountType.Debit),
            JournalEntryLeg(mortgage_account, 100, AmountType.Credit),
        ]
    )

    assert jnl.is_balanced()

    # Journal entry is not balanced if Debit != Credit
    jnl = JournalEntry(
        [
            JournalEntryLeg(cash_account, 100, AmountType.Debit),
            JournalEntryLeg(mortgage_account, 50, AmountType.Credit),
        ]
    )

    assert not jnl.is_balanced()

    # Journal entry is not balanced even if posting negative amounts
    jnl = JournalEntry(
        [
            JournalEntryLeg(cash_account, 100, AmountType.Debit),
            JournalEntryLeg(mortgage_account, -100, AmountType.Debit),
        ]
    )

    assert not jnl.is_balanced()

    # Test floating-point precision 
    jnl = JournalEntry(
        [
            JournalEntryLeg(cash_account, 100, AmountType.Debit),
            JournalEntryLeg(mortgage_account, 99.9, AmountType.Credit),
        ]
    )
    
    assert not jnl.is_balanced()
