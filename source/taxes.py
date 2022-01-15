#!/usr/bin/env python3

import sys
import slet

class Credit:
    def __init__(self, value):
        self.value = value


################################################################################
# Alabama
################################################################################

class Alabama:
    deductions = {
        'single': 2500,
        'married': 7500
    }
    exemptions = {
        'personal': 1500,
        'dependant': 1000
    }
    brackets = {
        'single': [
            (0,      0, 0.02),
            (500,   10, 0.04),
            (3000, 110, 0.05),
        ],
        'married': [
            (0,      0, 0.02),
            (1000,  20, 0.04),
            (6000, 220, 0.05),
        ]
    }

################################################################################
# Arkansas
################################################################################

class Arkansas:
    deductions = {
        'single': 2200,
        'married': 4400
    }
    exemptions = {
        'personal': Credit(26),
        'dependant': Credit(26)
    }
    brackets = {
        'single': [
            (0,           0, 0.02),
            (4000,    80.00, 0.04),
            (8000,   240.00, 0.059),
            (79300, 4446.70, 0.066),
        ],
        'married': [
            (0,           0, 0.02),
            (4000,    80.00, 0.04),
            (8000,   240.00, 0.059),
            (79300, 4446.70, 0.066),
        ]
    }

################################################################################
# Arizona
################################################################################

class Arizona:
    deductions = {
        'single': 5312,
        'married': 10613
    }
    exemptions = {
        'personal': 2200,
        'dependant': 2300
    }
    brackets = {
        'single': [
            (0,             0, 0.0259),
            (26500,    686.35, 0.0334),
            (53000,   1571.45, 0.0417),
            (159000,  5991.65, 0.0450),
        ],
        'married': [
            (0,             0, 0.0259),
            (53000,   1372.70, 0.0334),
            (106000,  3142.90, 0.0417),
            (318000, 11983.30, 0.0450),
        ]
    }

################################################################################
# California
################################################################################

class California:
    deductions = {
        'single': 4236,
        'married': 8472
    }
    exemptions = {
        'personal': Credit(114),
        'dependant': Credit(353)
    }
    brackets = {
        'single': [
            (0,            0.00, 0.010),
            (8809,        88.09, 0.020),
            (20883,      329.57, 0.040),
            (32960,      812.65, 0.060),
            (45753,     1580.23, 0.080),
            (57824,     2545.91, 0.093),
            (295373,   24637.97, 0.103),
            (354445,   30722.38, 0.113),
            (590742,   57423.94, 0.123),
            (1000000, 107762.68, 0.133),
        ],
        'married': [
            (0,            0.00, 0.010),
            (17618,      176.18, 0.020),
            (41766,      659.14, 0.040),
            (65920,     1625.30, 0.060),
            (91506,     3160.46, 0.080),
            (115648,    5091.82, 0.093),
            (590746,   49275.93, 0.103),
            (708890,   61444.77, 0.113),
            (1000000,  94340.20, 0.123),
            (1181484, 116662.73, 0.133),
        ]
    }

################################################################################
# Colorado
################################################################################

class Colorado:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 0,
        'dependant': 0
    }
    brackets = {
        'single': [
            (0, 0, 0.0463),
        ],
        'married': [
            (0, 0, 0.0463),
        ]
    }

################################################################################
# Connecticut
################################################################################

class Connecticut:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': Credit(15000),
        'dependant': 0
    }
    brackets = {
        'single': [
            (0,           0, 0.0300),
            (10000,     300, 0.0500),
            (50000,    2300, 0.0550),
            (100000,   5050, 0.0600),
            (200000,  11050, 0.0650),
            (250000,  14300, 0.0690),
            (500000,  31550, 0.0699),
        ],
        'married': [
            (0,           0, 0.0300),
            (20000,     300, 0.0500),
            (100000,   2300, 0.0550),
            (200000,   5050, 0.0600),
            (400000,  11050, 0.0650),
            (500000,  14300, 0.0690),
            (1000000, 31550, 0.0699),
        ]
    }

################################################################################
# Delaware
################################################################################

class Delaware:
    deductions = {
        'single': 3250,
        'married': 6500
    }
    exemptions = {
        'personal': Credit(110),
        'dependant': Credit(110)
    }
    brackets = {
        'single': [
            (0,         0.00, 0.0000),
            (2000,      0.00, 0.0220),
            (5000,     66.00, 0.0390),
            (10000,   261.00, 0.0480),
            (20000,   741.00, 0.0520),
            (25000,  1001.00, 0.0555),
            (60000,  2943.50, 0.0660),
        ],
        'married': [
            (0,         0.00, 0.0000),
            (2000,      0.00, 0.0220),
            (5000,     66.00, 0.0390),
            (10000,   261.00, 0.0480),
            (20000,   741.00, 0.0520),
            (25000,  1001.00, 0.0555),
            (60000,  2943.50, 0.0660),
        ]
    }

################################################################################
# District of Columbia
################################################################################

class DistrictOfColumbia:
    deductions = {
        'single': 12000,
        'married': 24000
    }
    exemptions = {
        'personal': 0,
        'dependant': 0
    }
    brackets = {
        'single': [
            (0,           0.00, 0.0400),
            (10000,     400.00, 0.0600),
            (40000,    2200.00, 0.0650),
            (60000,    3500.00, 0.0850),
            (350000,  28150.00, 0.0875),
            (1000000, 85025.00, 0.0895),
        ],
        'married': [
            (0,           0.00, 0.0400),
            (10000,     400.00, 0.0600),
            (40000,    2200.00, 0.0650),
            (60000,    3500.00, 0.0850),
            (350000,  28150.00, 0.0875),
            (1000000, 85025.00, 0.0895),
        ]
    }

################################################################################
# Georgia
################################################################################

class Georgia:
    deductions = {
        'single': 4600,
        'married': 6000
    }
    exemptions = {
        'personal': 2700,
        'dependant': 3000
    }
    brackets = {
        'single': [
            (0,      0.00, 0.0100),
            (750,    7.50, 0.0200),
            (2250,  37.50, 0.0300),
            (3750,  82.50, 0.0400),
            (5250, 142.50, 0.0500),
            (7000, 230.00, 0.0575),
        ],
        'married': [
            (0,       0.00, 0.0100),
            (1000,   10.00, 0.0200),
            (3000,   50.00, 0.0300),
            (5000,  110.00, 0.0400),
            (7000,  190.00, 0.0500),
            (10000, 340.00, 0.0575),
        ]
    }

states = {
        'AK': None,
        'AL': Alabama,
        'AR': Arkansas,
        'AZ': Arizona,
        'CA': California,
        'CO': Colorado,
        'CT': Connecticut,
        'DE': Delaware,
        'DC': DistrictOfColumbia,
        'FL': None,
}

todo = {
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def calculate_state_taxes(agi, married, state, dependants=0):
    assert agi >= 0
    if agi == 0 or states[state] is None:
        return 0

    if married:
        brackets = states[state].brackets['married']
        deduction = states[state].deductions['married']
    else:
        brackets = states[state].brackets['single']
        deduction = states[state].deductions['single']

    taxes = 0
    taxable_income = agi - deduction

    #
    # Handle personal exemptions.
    #
    multiplier = 2 if married else 1
    personal_exemption = states[state].exemptions['personal']
    if isinstance(personal_exemption, Credit):
        taxes -= personal_exemption.value * multiplier
    else:
        taxable_income -= personal_exemption * multiplier

    #
    # Handle dependants.
    #
    dependant_exemption = states[state].exemptions['dependant']
    if isinstance(dependant_exemption, Credit):
        taxes -= dependant_exemption.value * dependants
    else:
        taxable_income -= dependant_exemption * dependants

    #
    # Calculate taxes.
    #
    for minimum, base_tax, tax_rate in reversed(brackets):
        if taxable_income > minimum:
            taxes += base_tax + ((taxable_income - minimum) * tax_rate)
            return max(taxes, 0)

    return 0

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

def calculate_estate_taxes(estate):
    assert estate > 0
    deduction = 11700000 # $11.7 million for 2021
    taxable_estate = max(0, estate - deduction)
    if not taxable_estate:
        return 0

    for minimum, base_tax, tax_rate in reversed(estate_tax_brackets):
        if taxable_estate > minimum:
            return base_tax + ((taxable_estate - minimum) * tax_rate)

def calculate_minimum_remaining_taxes_for_heir(value, age):
    total_taxes = 0
    while True:
        try:
            rmd = value/slet.withdrawal_factors[age]
            value -= rmd
            total_taxes += calculate_taxes(rmd, True)
        except KeyError:
            break
        age += 1
    return total_taxes

def get_standard_deduction(married):
    return 24800 if married else 12400

def calculate_taxes(agi, married, state=None, ltcg=0, just_ltcg=False, debug=False):
    def debug_print(line):
        if debug:
            print(line)

    assert agi >= 0, f"{agi=:.2f}"
    debug_print("Calculating federal income tax")
    standard_deduction = get_standard_deduction(married)
    income_to_tax = max(agi - standard_deduction, 0)
    income_taxes = 0.0
    brackets = married_tax_brackets if married else single_tax_brackets
    for tax_rate, rate_limit in brackets:
        taxable_income_at_rate = min(income_to_tax, rate_limit)
        taxes_at_rate = tax_rate * taxable_income_at_rate
        debug_print(f"{tax_rate=:.2f} * {taxable_income_at_rate=:10,.2f} = {taxes_at_rate=:10,.2f}")
        income_taxes += taxes_at_rate
        income_to_tax -= taxable_income_at_rate
        if income_to_tax == 0:
            break

    if state:
        state_income_taxes = calculate_state_taxes(agi, married, state)
        debug_print(f"${state_income_taxes:,.2f}\n")
        income_taxes += state_income_taxes

    debug_print(f"============================================================================")
    debug_print(f"Total: ${income_taxes:,.2f}\n")

    debug_print("Calculating long-term capital gains tax")
    income_to_tax = ltcg
    ltcg_taxes = 0
    taxed_income = 0
    brackets = married_ltcg_brackets if married else single_ltcg_brackets
    for tax_rate, rate_limit in brackets:
        if taxed_income < agi:
            taxable_income_at_rate = min((agi - taxed_income), rate_limit)
            debug_print(f"{tax_rate=:.2f} * {taxable_income_at_rate=:10,.2f} = skipping agi")
            taxed_income += taxable_income_at_rate
            rate_limit -= taxable_income_at_rate
            if ((agi - taxed_income) > 0):
                continue
            if not rate_limit:
                continue

        taxable_income_at_rate = min(income_to_tax, rate_limit)
        taxes_at_rate = tax_rate * taxable_income_at_rate
        debug_print(f"{tax_rate=:.2f} * {taxable_income_at_rate=:10,.2f} = {taxes_at_rate=:10,.2f}")
        ltcg_taxes += taxes_at_rate
        income_to_tax -= taxable_income_at_rate
        taxed_income += taxable_income_at_rate
        if income_to_tax == 0:
            break
    debug_print(f"============================================================================")
    debug_print(f"Total: ${ltcg_taxes:,.2f}\n")

    if just_ltcg:
        return ltcg_taxes
    else:
        return income_taxes + ltcg_taxes

def fully_tax_deductible_ira(agi, married):
    limit = 104000 if married else 65000
    return agi < limit
