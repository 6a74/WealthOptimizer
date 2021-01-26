#!/usr/bin/env python3

class Withdrawal:
    """
    This class represents a withdrawal. It stores relevant information.
    Withdrawals can be insufficient.
    """
    def __init__(self, value, gains, insufficient=0):
        self.value = value
        self.gains = gains
        self.insufficient = insufficient

    def __repr__(self):
        return (
            f"Withdrawal(value={self.value:,.2f}"
            + f" gains={self.gains:,.2f}"
            + (f" insufficient={self.insufficient:,.2f}" if self.insufficient else "")
            + ")"
        )

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
    def __init__(self, rate_of_return, withdrawal_contributions_first=False):
        self.rate_of_return = rate_of_return
        self.withdrawal_contributions_first = withdrawal_contributions_first
        self.account_age = 0
        self.contributions = 0
        self.value = 0

    def __repr__(self):
        return (
            f"Account(age={self.account_age:d}"
            f" value={self.get_value():,.2f}"
            f" gains={self.get_gains():,.2f}"
            f" contrs_first={self.withdrawal_contributions_first}"
            f")"
        )

    def contribute(self, money):
        self.contributions += money
        self.value += money

    def get_value(self):
        return self.value

    def get_contributions(self):
        return self.contributions

    def has_contributions(self):
        return bool(self.contributions)

    def get_gains(self):
        return self.get_value() - self.get_contributions()

    def get_gains_ratio(self):
        return self.get_gains()/self.get_value()

    def withdrawal(self, needed, dry_run=False):
        assert needed >= 0
        total_taken = 0
        still_needed = needed
        total_gains = 0

        # Back up these values in case it's a dry run.
        value, contributions = self.value, self.contributions

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
            self.contributions -= to_take * (1 - ratio)

            total_taken += to_take
            total_gains += to_take * ratio
            still_needed -= to_take

        if dry_run:
            self.value, self.contributions = value, contributions

        return Withdrawal(total_taken, total_gains, still_needed)

    def increment(self):
        self.account_age += 1
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
