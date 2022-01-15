#!/usr/bin/env python3

class Asset(object):
    """
    This class represents an asset.
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

    def get_gains(self):
        return self.value - self.basis

    def increment(self, interest_rate):
        self.age += 1
        self.value *= interest_rate
        self.value = round(self.value, 2)


class Account:
    """
    This class represents an account. It holds assets.
    """
    def __init__(self, rate_of_return, withdrawal_contributions_first=False):
        self.rate_of_return = rate_of_return
        self.withdrawal_contributions_first = withdrawal_contributions_first
        self.account_age = 0
        self.assets = []

    def __repr__(self):
        lines = []
        lines.append(f"Account(age={self.account_age:d} value={self.get_value():,.2f} gains={self.get_gains():,.2f})")
        for asset in self.assets:
            lines.append("\t" + repr(asset))
        return "\n".join(lines)

    def contribute(self, money):
        self.assets.insert(0, Asset(money))

    def get_value(self):
        return sum(a.get_value() for a in self.assets)

    def get_contributions(self):
        return sum(a.get_basis() for a in self.assets)

    def has_contributions(self):
        return bool(self.get_contributions())

    def get_gains(self):
        return self.get_value() - self.get_contributions()

    def get_gains_ratio(self):
        return self.get_gains()/self.get_value()

    def withdrawal(self, needed):
        assert needed >= 0
        total_taken = 0
        still_needed = needed
        total_gains = 0

        while round(still_needed, 2):

            #
            # If our account has nothing in it, there's no point in trying. Just
            # return what we were able to get, if anything.
            #
            if not self.get_value():
                break

            for asset in self.assets:
                to_take = min(still_needed, asset.get_value())
                if self.withdrawal_contributions_first \
                        and self.has_contributions():
                    to_take = min(still_needed, asset.get_basis())

                #
                # TODO: Double check that this is right.
                #
                ratio = asset.get_gains()/asset.get_value()
                if self.withdrawal_contributions_first \
                        and self.has_contributions():
                    ratio = 0.0

                asset.value -= to_take
                asset.basis -= asset.get_basis() * (1 - ratio)
                still_needed -= to_take
                total_taken += to_take
                total_gains += to_take * ratio

            #
            # Remove assets that have no value. No point in keeping them around.
            #
            non_zero_assets = []
            for asset in self.assets:
                if round(asset.get_value(), 2):
                    non_zero_assets.append(asset)
            self.assets = non_zero_assets

        #
        # Return the gains too, so we know if we need to pay taxes.
        #
        return total_taken, total_gains

    def increment(self):
        self.account_age += 1
        for asset in self.assets:
            asset.increment(self.rate_of_return)


if __name__ == "__main__":
    account = Account(1.06, withdrawal_contributions_first=False)

    account.contribute(100.00)
    account.increment()
    account.contribute(200.00)
    account.increment()
    account.contribute(300.00)
    account.increment()
    account.contribute(100.00)

    print("before")
    print(account)

    withdrawal = account.withdrawal(100)
    print(f"got {withdrawal[0]:,.2f}, gains: {withdrawal[1]:,.2f}")

    print("after")
    print(account)
