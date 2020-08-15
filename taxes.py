#!/usr/bin/env python3

import sys

#
# These brackets are a bit weird, but it's the amount of money in each tax
# bracket bucket, rather than income limits.
#

single_tax_brackets = [
    (0.10,   9875),
    (0.12,  30250), #  40,125
    (0.22,  45400), #  85,525
    (0.24,  77805), # 163,330
    (0.32,  44020), # 207,350
    (0.35, 311050), # 518,400
    (0.37, sys.float_info.max),
]

married_tax_brackets = [
    (0.10,  19750),
    (0.12,  60500), #  80,250
    (0.22,  90800), # 171,050
    (0.24, 155550), # 326,600
    (0.32,  88100), # 414,700
    (0.35, 207350), # 622,050
    (0.37, sys.float_info.max),
]

def calculate_taxes(income, married, debug=False):
    #
    # The 2020 standard deductions.
    #
    standard_deduction = 24800 if married else 12400
    income -= standard_deduction

    #
    # Can't have a negative income :)
    #
    income = max(income, 0)

    #
    # Which bracket do we use?
    #
    brackets = married_tax_brackets if married else single_tax_brackets

    taxes = 0.0
    for tax_rate, rate_limit in brackets:
        taxable_income_at_rate = min(income, rate_limit)
        taxes_at_rate = tax_rate * taxable_income_at_rate
        if debug:
            print(f"{tax_rate=:.2f} * {taxable_income_at_rate=:10,.2f} = {taxes_at_rate=:10,.2f}")
        taxes += taxes_at_rate
        income -= taxable_income_at_rate

    return taxes

def get_capital_gains_tax_rate(income, married, debug=False):
    if not married:
        if income < 40000:
            return 0.00
        elif income < 441450:
            return 0.15
        else:
            return 0.20
    else:
        if income < 800000:
            return 0.00
        elif income < 496050:
            return 0.15
        else:
            return 0.20
