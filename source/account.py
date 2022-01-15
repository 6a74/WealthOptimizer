#!/usr/bin/env python3

import math

class Asset(object):
    """
    """

    def __init__(self, contribution):
        self.age = 0
        self.basis = contribution
        self.value = contribution

    def __repr__(self):
        return f"Asset(age={self.age:d} basis={self.basis=:.2f} value={self.value=:.2f})"

    def get_basis(self):
        return self.basis

    def get_value(self):
        return self.value

    def increment(self, interest_rate):
        self.age += 1
        self.value *= interest_rate


class Account(object):
    """
    """

    def __init__(self, withdrawal_contributions_first=False):
        self.withdrawal_contributions_first = withdrawal_contributions_first
        self.account_age = 0
        self.assets = []

    def __repr__(self):
        lines = []
        lines.append(f"Asset(age={self.account_age:d} value={self.get_value():,.2f})")
        for index, asset in enumerate(self.assets):
            lines.append(f"\t{index=} {asset=}")
        return "\n".join(lines)

    def contribute(self, money):
        self.assets.append(Asset(money))

    def get_value(self):
        return sum(a.get_value() for a in self.assets)

    def get_contributions(self):
        return sum(a.get_basis() for a in self.assets)

    def get_earnings_ratio(self):
        earnings = self.get_value() - self.get_contributions()
        return earnings/self.get_value()

    def withdrawal(self, needed):
        assert needed >= 0
        total_taken = 0
        still_needed = needed

        #
        #
        #
        for asset in self.assets:
            to_take = min(still_needed, asset.get_value())
            asset.value -= to_take
            asset.basis -= to_take * (1 - self.get_earnings_ratio())
            still_needed -= to_take
            total_taken += to_take

            if math.isclose(total_taken, needed):
                break

        #
        #
        #
        non_zero_assets = []
        for asset in self.assets:
            if not math.isclose(asset.get_value(), 0):
                non_zero_assets.append(asset)
        self.assets = non_zero_assets

        #
        #
        #
        return total_taken

    def increment(self, interest_rate):
        self.account_age += 1
        for asset in self.assets:
            asset.increment(interest_rate)



if __name__ == "__main__":
    #
    # Testing:
    #
    account = Account()

    account.contribute(100.00)
    account.increment(1.06)
    account.contribute(200.00)
    account.increment(1.06)
    account.contribute(300.00)
    account.increment(1.06)
    account.contribute(100.00)

    print("before")
    print(account)

    withdrawal = account.withdrawal(50)
    print(f"{withdrawal=:.2f}")

    print("after")
    print(account)
