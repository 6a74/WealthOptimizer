#!/usr/bin/env python3

import sys
import slet

class FederalIncomeTax_2021:
    deductions = {
        'single': 12550,
        'married': 25100
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (     0,      0.00, 0.10),
            (  9950,    995.00, 0.12),
            ( 40525,   4664.00, 0.22),
            ( 86375,  14751.00, 0.24),
            (164925,  33603.00, 0.32),
            (209425,  47843.00, 0.35),
            (523600, 157804.25, 0.37),
        ],
        'married': [
            (     0,      0.00, 0.10),
            ( 19900,   1990.00, 0.12),
            ( 81050,   9328.00, 0.22),
            (172750,  29502.00, 0.24),
            (329850,  67206.00, 0.32),
            (418850,  95686.00, 0.35),
            (628300, 168993.50, 0.37),
        ]
    }

single_ltcg_brackets = [
    (0.00,   40000),
    (0.15,  401450), # 441,450
    (0.20, sys.float_info.max),
]

married_ltcg_brackets = [
    (0.00,   80000),
    (0.15,  416600), # 496,600
    (0.20, sys.float_info.max),
]

estate_tax_brackets = [
    (0,       0,      0.18),
    (10000,   1800,   0.20),
    (20000,   3800,   0.22),
    (40000,   8200,   0.24),
    (60000,   13000,  0.26),
    (80000,   18200,  0.28),
    (100000,  23800,  0.30),
    (150000,  38800,  0.32),
    (250000,  70800,  0.34),
    (500000,  155800, 0.37),
    (750000,  248300, 0.39),
    (1000000, 345800, 0.40),
]

savers_credit_brackets_married = [
    (0,     0.50),
    (39501, 0.20),
    (43001, 0.10),
    (66000, 0.00),
]

savers_credit_brackets_other = [
    (0,     0.50),
    (19751, 0.20),
    (21501, 0.10),
    (33000, 0.00),
]

def calculate_savers_credit(agi, retirement_contributions, married):
    assert agi >= 0
    qualified_retirement_contributions = min(4000 if married else 2000, retirement_contributions)
    bracket = savers_credit_brackets_married if married else savers_credit_brackets_other
    for limit, credit_rate in reversed(bracket):
        if agi >= limit:
            return qualified_retirement_contributions * credit_rate

def calculate_estate_tax(estate):
    assert estate >= 0
    deduction = 11700000 # $11.7 million for 2021
    taxable_estate = max(0, estate - deduction)
    if not taxable_estate:
        return 0

    for minimum, base_tax, tax_rate in reversed(estate_tax_brackets):
        if taxable_estate > minimum:
            return base_tax + ((taxable_estate - minimum) * tax_rate)

def calculate_minimum_remaining_tax_for_heir(value, age):
    total_taxes = 0
    while True:
        try:
            rmd = value/slet.withdrawal_factors[age]
            value -= rmd
            total_taxes += calculate_federal_income_tax(rmd, True)
        except KeyError:
            break
        age += 1
    return total_taxes

def get_standard_deduction(married):
    key = 'married' if married else 'single'
    return FederalIncomeTax_2021.deductions[key]

def calculate_fica_tax(gross_income, married):
    assert gross_income >= 0
    # This is the 2021 limit.
    social_security_tax = min(142800, gross_income) * 0.062
    medicare_tax = gross_income * 0.0145
    threshold = 250000 if married else 200000
    additional_medicare_tax = max(gross_income - threshold, 0) * 0.009
    return social_security_tax + medicare_tax + additional_medicare_tax

def calculate_federal_income_tax(agi, married, dependents=0, ltcg=0, just_ltcg=False):
    assert agi >= 0, f"{agi=:.2f}"

    standard_deduction = get_standard_deduction(married)
    income_to_tax = max(agi - standard_deduction, 0)
    key = 'married' if married else 'single'
    brackets = FederalIncomeTax_2021.brackets[key]

    income_taxes = 0
    for minimum, base_tax, tax_rate in reversed(brackets):
        if income_to_tax > minimum:
            income_taxes += base_tax + ((income_to_tax - minimum) * tax_rate)
            break

    income_to_tax = ltcg
    ltcg_taxes = 0
    taxed_income = 0
    brackets = married_ltcg_brackets if married else single_ltcg_brackets
    for tax_rate, rate_limit in brackets:
        if taxed_income < agi:
            taxable_income_at_rate = min((agi - taxed_income), rate_limit)
            taxed_income += taxable_income_at_rate
            rate_limit -= taxable_income_at_rate
            if ((agi - taxed_income) > 0):
                continue
            if not rate_limit:
                continue

        taxable_income_at_rate = min(income_to_tax, rate_limit)
        taxes_at_rate = tax_rate * taxable_income_at_rate
        ltcg_taxes += taxes_at_rate
        income_to_tax -= taxable_income_at_rate
        taxed_income += taxable_income_at_rate
        if income_to_tax == 0:
            break

    if just_ltcg:
        return ltcg_taxes
    else:
        return income_taxes + ltcg_taxes

def fully_tax_deductible_ira(agi, married):
    limit = 104000 if married else 65000
    return agi < limit
