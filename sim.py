#!/usr/local/bin/python3

import argparse
import ult
import taxes as tm

class Asset(object):
    basis = 0
    value = 0

    def __init__(self, contribution):
        basis = contribution
        value = contribution

    def get_basis(self):
        return basis

    def get_gains(self):
        return value - basis

    def get_value(self):
        return value

    def increment(self, interest_rate):
        value *= interest_rate
        pass

class Ledger(object):
    ledger = []

    def contribute(self, money):
        ledger.append(Asset(money))

    def withdrawal(self, money):
        basis, gains = 0, 0
        while basis + gains < money:
            pass

    def increment():
        age += 1

def calculate_tax_to_asset_ratio(traditional, roth, interest_rate,
                   yearly_contribution_traditional, yearly_contribution_roth,
                   years_until_transition_to_pretax_contributions, current_age,
                   age_of_retirement, age_to_start_rmds, age_of_death,
                   roth_conversion_amount, income, yearly_income_raise,
                   max_income, age_of_marriage,
                   max_yearly_contribution_traditional,
                   max_yearly_contribution_roth, yearly_retirement_spending,
                   debug=True):
    """This function will simulate the state of finances for each year until you
    die, depending on the inputs of course!
    """

    def debug_print(line):
        if debug:
            print(line)

    assert current_age <= 115
    assert current_age < age_of_death

    debug_print(f"{current_age=}")
    debug_print(f"{age_of_death=}")
    debug_print(f"{age_of_marriage=}")
    debug_print(f"{age_of_retirement=}")
    debug_print(f"{age_to_start_rmds=}")
    debug_print(f"{income=:,.2f}")
    debug_print(f"{max_income=:,.2f}")
    debug_print(f"{interest_rate=:.2f}")
    debug_print(f"{yearly_income_raise=:.2f}")
    debug_print(f"{roth=:,.2f}")
    debug_print(f"{traditional=:,.2f}")
    debug_print(f"{yearly_contribution_roth=:,.2f}")
    debug_print(f"{max_yearly_contribution_roth=:,.2f}")
    debug_print(f"{yearly_contribution_traditional=:,.2f}")
    debug_print(f"{max_yearly_contribution_traditional=:,.2f}")
    debug_print(f"{roth_conversion_amount=:,.2f}")
    debug_print(f"{years_until_transition_to_pretax_contributions=}")
    debug_print(f"{yearly_retirement_spending=:,.2f}")
    debug_print("")

    taxes = 0
    taxable = 0
    taxable_principal = 0
    total_contributions_traditional = 0
    total_contributions_roth = 0
    total_contributions_taxable = 0
    total_taxes = 0

    #
    # Doesn't really help me, but y'all might already be married.
    #
    married = True if age_of_marriage <= current_age else False

    debug_print(f"|| Age ||       Taxable ||          Roth ||   Traditional ||  Total Assets ||         RMD ||   Spending ||  Tax Cont. || Roth Cont. || Trad Cont. ||       MAGI ||      Taxes || Tax % ||  Total Taxes ||")
    debug_print(f"===========================================================================================================================================================================================")

    #
    # Iterate over each year in our life.
    #
    for year in range(age_of_death - current_age):
        #
        # Print some major life status updates.
        #
        if year == years_until_transition_to_pretax_contributions:
            if current_age < age_of_retirement:
                debug_print("you're starting pretax contributions")

        if current_age == age_to_start_rmds:
            debug_print("you have rmds now")

        if current_age == age_of_retirement:
            debug_print("you're now retired, stopping contributions{}".format(
                ", doing roth conversions" if roth_conversion_amount else ""
            ))

        if current_age == age_of_marriage:
            debug_print("you're now married")
            married = True

        #
        # Alright, if we're still working, we can make a tax-advantaged
        # contribution of some type. This might include tax deductions.
        #
        roth_contrib = 0
        trad_contrib = 0
        taxable_contrib = 0
        tax_deductions = 0
        this_years_income = 0
        retirement_salary = 0

        if current_age < age_of_retirement:
            #
            # We are still working.
            #
            this_years_income = income
            total_contributions_roth += yearly_contribution_roth
            roth += yearly_contribution_roth
            roth_contrib += yearly_contribution_roth

            if year >= years_until_transition_to_pretax_contributions:
                total_contributions_traditional += yearly_contribution_traditional
                traditional += yearly_contribution_traditional
                tax_deductions += yearly_contribution_traditional
                trad_contrib = yearly_contribution_traditional

                #
                # Calculate how much we saved in taxes.
                #
                _taxable_income = this_years_income
                assert _taxable_income >= 0
                taxes_without = tm.calculate_taxes(_taxable_income, married)

                _taxable_income = this_years_income - tax_deductions
                assert _taxable_income >= 0
                taxes_with = tm.calculate_taxes(_taxable_income, married)

                #
                # Put the difference in a taxable account.
                #
                difference = taxes_without - taxes_with
                taxable += difference
                taxable_contrib += difference
                total_contributions_taxable += difference
            else:
                #
                # We are diverting traditional to roth.
                #
                total_contributions_roth += yearly_contribution_traditional
                roth += yearly_contribution_traditional
                roth_contrib = yearly_contribution_traditional
        else:
            #
            # We have retired.
            #
            if current_age < age_to_start_rmds:
                roth_conversion_amount = min(traditional, roth_conversion_amount)
                this_years_income = roth_conversion_amount
                roth += roth_conversion_amount
                traditional -= roth_conversion_amount

        #
        # Do we need to make RMDs?
        #
        if current_age >= age_to_start_rmds:
            rmd = traditional/ult.withdrawal_factors[current_age]
            best_amount = tm.get_standard_deduction(married)
            withdrawal_amount = max(rmd, best_amount)
            if withdrawal_amount >= traditional:
                withdrawal_amount = traditional

            traditional -= withdrawal_amount
            this_years_income += withdrawal_amount

            money_still_needed_for_retirement = yearly_retirement_spending - retirement_salary
            if money_still_needed_for_retirement:
                money_for_retirement_salary = min(withdrawal_amount, money_still_needed_for_retirement)
                retirement_salary += money_for_retirement_salary
                money_for_taxable = withdrawal_amount - money_for_retirement_salary

            taxable_principal += money_for_taxable
            taxable += money_for_taxable
            total_contributions_taxable += money_for_taxable
            taxable_contrib += money_for_taxable
        else:
            rmd = 0

        #
        # Do we need to take out more money for retirement?
        #
        #
        """
        if current_age >= age_of_retirement:
            money_still_needed_for_retirement = yearly_retirement_spending - retirement_salary
            if money_still_needed_for_retirement > 0:
                debug_print(f"{money_still_needed_for_retirement=:,.2f}")
                gains_to_pull_from_taxable = tm.max_withdrawal_taxable_no_capital_gains(married) - this_years_income
                gains = taxable - total_contributions_taxable
                if total_contributions_taxable:
                    taxable_return_rate = taxable/total_contributions_taxable
                    debug_print(f"{gains_to_pull_from_taxable=:,.2f} {gains=:,.2f} {taxable_return_rate=:,.2f}")
                    if gains_to_pull_from_taxable > 0:
                        percentage_to_pull = gains_to_pull_from_taxable/gains

                        #
                        # Sell percentage_to_pull of taxable.
                        #
                        taxable_withdrawal = taxable * percentage_to_pull
                
        """
                

        #
        # How much taxes are we going to pay this year?
        #
        taxable_income = this_years_income - tax_deductions
        assert taxable_income >= 0
        taxes = tm.calculate_taxes(taxable_income, married)
        total_taxes += taxes

        #
        # Calculate the effective tax rate.
        #
        try:
            tax_rate = (taxes/this_years_income) * 100
        except ZeroDivisionError:
            tax_rate = 0

        total_assets = taxable + roth + traditional
        debug_print(f"|| {current_age:3d} || {taxable:13,.2f} || {roth:13,.2f} || {traditional:13,.2f} || {total_assets:13,.2f} || {rmd:11,.2f} || {retirement_salary:10,.2f} || {taxable_contrib:10,.2f} || {roth_contrib:10,.2f} || {trad_contrib:10,.2f} || {taxable_income:10,.2f} || {taxes:10,.2f} || {tax_rate:5.2f} || {total_taxes:12,.2f} ||")

        #
        # Happy new year! It's the end of the year. Apply interest, give
        # yourself a pay raise, and happy birthday!
        #
        traditional *= interest_rate
        roth *= interest_rate
        taxable *= interest_rate

        if current_age < age_of_retirement:
            income *= yearly_income_raise
            if max_income:
                income = min(income, max_income)

            yearly_contribution_traditional *= yearly_income_raise
            if max_yearly_contribution_traditional:
                yearly_contribution_traditional = min(
                    yearly_contribution_traditional,
                    max_yearly_contribution_traditional
                )

            yearly_contribution_roth *= yearly_income_raise
            if max_yearly_contribution_roth:
                yearly_contribution_roth = min(
                    yearly_contribution_roth,
                    max_yearly_contribution_roth
                )

        current_age += 1

    #
    # Alright you are ABOUT to die. Time to sell everything.
    #
    debug_print("about to die, selling everything")

    taxable_gains = taxable - total_contributions_taxable
    debug_print(f"{taxable_gains=:,.2f}")

    #
    # Capital gains are taxed a differently.
    #
    debug_print(f"{taxable_income=:,.2f}")
    ltcg_taxes = tm.calculate_taxes(taxable_income, married, ltcg=taxable_gains, just_ltcg=True)
    debug_print(f"{ltcg_taxes=:,.2f}")
    
    whats_left = taxable_gains - ltcg_taxes
    debug_print(f"{whats_left=:,.2f}")
    total_taxes += ltcg_taxes
    total_assets = roth + traditional + whats_left
    debug_print(f"{total_taxes=:,.2f}")
    debug_print(f"{total_assets=:,.2f}")

    #
    # You're finally dead.
    #
    debug_print("congrats, you're dead")

    tax_to_asset_ratio = total_taxes/total_assets
    return tax_to_asset_ratio


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate RMDs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--current-age",
        help="Your current age",
        required=False,
        type=int,
        default=38
    )
    parser.add_argument(
        "--income",
        help="Your current income",
        required=False,
        type=float,
        default=63179
    )
    parser.add_argument(
        "--max-income",
        help="Define an income ceiling",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--principal-traditional",
        help="Starting balance for Traditional (pre-tax) accounts?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--principal-roth",
        help="Starting balance for Roth (after-tax) accounts?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--interest-rate",
        help="What is the long-term interest rate?",
        required=False,
        type=float,
        default=1.04
    )
    parser.add_argument(
        "--yearly-contribution-traditional",
        help="How much are you contributing to Traditional per year?",
        required=False,
        type=float,
        default=6000
    )
    parser.add_argument(
        "--max-yearly-contribution-traditional",
        help="What is the Traditional contribution limit?",
        required=False,
        type=float,
        default=19500
    )
    parser.add_argument(
        "--yearly-contribution-roth",
        help="How much are you contributing to Roth per year?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--max-yearly-contribution-roth",
        help="What is the Roth contribution limit?",
        required=False,
        type=float,
        default=6000
    )
    parser.add_argument(
        "--years-to-wait",
        help="Years to wait before doing Traditional (pre-tax) contributions",
        metavar="YEARS",
        required=False,
        type=int,
        default=0
    )
    parser.add_argument(
        "--age-of-retirement",
        help="When do you plan to retire?",
        required=False,
        type=int,
        default=60
    )
    parser.add_argument(
        "--age-to-start-rmds",
        help="When do RMDs start?",
        required=False,
        type=int,
        default=72
    )
    parser.add_argument(
        "--age-of-death",
        help="When do you plan on dying?",
        required=False,
        type=int,
        default=79
    )
    parser.add_argument(
        "--yearly-income-raise",
        help="How much of a raise are you expecting each year?",
        required=False,
        type=float,
        default=1.02
    )
    parser.add_argument(
        "--age-of-marriage",
        help="When will you get married?",
        required=False,
        type=int,
        default=30
    )
    parser.add_argument(
        "--yearly-retirement-spending",
        help="How much money will you need in retirement",
        required=False,
        type=float,
        default=30000
    )
    parser.add_argument(
        "--verbose",
        help="Do things and talk more",
        action="store_true"
    )

    args = parser.parse_args()

    #
    # Calculate the most efficient Roth conversion amount.
    #
    min_tax_rate = 1.0
    roth_conversion_amount = 0
    best_roth_conversion_amount = 0

    #
    # There's a chance we could die before retirement.
    #
    if args.age_of_death > args.age_of_retirement:
        for x in range(1000):
            tax_rate = calculate_tax_to_asset_ratio(
                args.principal_traditional,
                args.principal_roth,
                args.interest_rate,
                args.yearly_contribution_traditional,
                args.yearly_contribution_roth,
                args.years_to_wait,
                args.current_age,
                args.age_of_retirement,
                args.age_to_start_rmds,
                args.age_of_death,
                roth_conversion_amount,
                args.income,
                args.yearly_income_raise,
                args.max_income,
                args.age_of_marriage,
                args.max_yearly_contribution_traditional,
                args.max_yearly_contribution_roth,
                args.yearly_retirement_spending,
                debug=False
            )
            if tax_rate < min_tax_rate:
                best_roth_conversion_amount = roth_conversion_amount
            min_tax_rate = min(min_tax_rate, tax_rate)
            """
            if tax_rate > min_tax_rate:
                break
            """
            roth_conversion_amount += 1000

    #
    # Now that we know all of the variables, run the simulation.
    #
    tax_to_asset_ratio = calculate_tax_to_asset_ratio(
        args.principal_traditional,
        args.principal_roth,
        args.interest_rate,
        args.yearly_contribution_traditional,
        args.yearly_contribution_roth,
        args.years_to_wait,
        args.current_age,
        args.age_of_retirement,
        args.age_to_start_rmds,
        args.age_of_death,
        best_roth_conversion_amount,
        args.income,
        args.yearly_income_raise,
        args.max_income,
        args.age_of_marriage,
        args.max_yearly_contribution_traditional,
        args.max_yearly_contribution_roth,
        args.yearly_retirement_spending,
        args.verbose
    )

    print(f"{tax_to_asset_ratio=:.6f}")
