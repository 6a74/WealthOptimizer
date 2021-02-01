#!/usr/bin/env python3
#
import rich

class Withdrawal:
    """
    This class represents a withdrawal. It stores relevant information.
    Withdrawals can be insufficient.
    """
    def __init__(self, account_name, value, gains, insufficient=0):
        self.account_name = account_name
        self.value = value
        self.gains = gains
        self.insufficient = insufficient

    def __repr__(self):
        return (
            f"Withdrawal(account={repr(self.account_name)}"
            + f" value={self.value:,.2f}"
            + f" gains={self.gains:,.2f}"
            + (f" insufficient={self.insufficient:,.2f}" if self.insufficient else "")
            + ")"
        )

    def get_account_name(self):
        return self.account

    def get_value(self):
        return self.value

    def get_gains(self):
        return self.gains

    def get_insufficient(self):
        return self.insufficient

class Account:
    """
    This class represents an account. It holds assets.
    """
    def __init__(self, name, rate_of_return, starting_balance=0,
                 withdrawal_contributions_first=False):
        self.name = name
        self.rate_of_return = rate_of_return
        self.withdrawal_contributions_first = withdrawal_contributions_first
        self.account_age = 0
        self.basis = 0
        self.contributions = 0
        self.value = starting_balance
        self.yearly_diff = [0]

    def __repr__(self):
        return (
            f"Account(name={repr(self.name)}"
            f" age={self.account_age:d}"
            f" value={self.get_value():,.2f}"
            f" basis={self.get_basis():,.2f}"
            f" gains={self.get_gains():,.2f}"
            f" conts={self.get_contributions():,.2f}"
            f" contrs_first={self.withdrawal_contributions_first}"
            f")"
        )

    def get_name(self):
        return self.name

    def contribute(self, money, rollover=False):
        money = round(money, 2)
        assert money >= 0, money
        self.basis += money
        self.value += money
        self.yearly_diff[self.account_age] += money
        if not rollover:
            self.contributions += money

    def get_value(self):
        return self.value

    def get_basis(self):
        return self.basis

    def get_contributions(self):
        return self.contributions

    def has_contributions(self):
        return bool(self.contributions)

    def get_gains(self):
        return self.get_value() - self.get_basis()

    def get_gains_ratio(self):
        return self.get_gains()/self.get_value()

    def get_yearly_diff(self):
        if self.yearly_diff[self.account_age] < 0:
            return f"[red]{self.yearly_diff[self.account_age]:+,.2f}[/red]"
        if self.yearly_diff[self.account_age] > 0:
            return f"[green]{self.yearly_diff[self.account_age]:+,.2f}[/green]"
        return ""

    def withdrawal(self, needed, dry_run=False):
        needed = round(needed, 2)
        assert needed >= 0, needed
        total_taken = 0
        still_needed = needed
        total_gains = 0

        # Back up these values in case it's a dry run.
        value, basis, conts = self.value, self.basis, self.contributions

        while round(still_needed, 2):
            #
            # If our account has nothing in it, there's no point in trying. Just
            # return what we were able to get, if anything.
            #
            if not self.get_value():
                break

            to_take = min(still_needed, self.get_value())
            if self.withdrawal_contributions_first and self.has_contributions():
                to_take = min(still_needed, self.get_contributions())

            ratio = self.get_gains()/self.get_value()
            if self.withdrawal_contributions_first and self.has_contributions():
                ratio = 0.0

            self.value -= to_take
            self.basis -= to_take * (1 - ratio)
            self.contributions -= to_take * (1 - ratio)
            self.contributions = max(self.contributions, 0)

            total_taken += to_take
            total_gains += to_take * ratio
            still_needed -= to_take

        if dry_run:
            self.value, self.basis, self.contributions = value, basis, conts
        if not dry_run:
            self.yearly_diff[self.account_age] -= total_taken

        return Withdrawal(
            self.get_name(),
            total_taken,
            total_gains,
            round(still_needed, 2)
        )

    def increment(self):
        self.account_age += 1
        self.yearly_diff.append(0)

        #
        # If the account is empty, there's a chance the value will become 0.01
        # with compounded interest. This looks bad.
        #
        if round(self.value, 2) == 0:
            self.value = 0
            self.basis = 0
            self.contributions = 0
        else:
            self.value *= self.rate_of_return


if __name__ == "__main__":
    account = Account(1.06, withdrawal_contributions_first=False)

    account.contribute(100.00)
    account.increment()
    account.contribute(200.00)
    account.increment()
    account.contribute(300.00)
    account.increment()
    account.contribute(100.00)

    print(account)
    print(account.withdrawal(1500))
    print(account)
