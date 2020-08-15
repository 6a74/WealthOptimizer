#!/usr/local/bin/python3

import argparse

from taxes import calculate_taxes
from ult import withdrawal_factors

def calculate_rmds(traditional, roth, interest_rate,
                   yearly_contribution_traditional, yearly_contribution_roth,
                   years_until_transition_to_pretax_contributions, current_age,
                   age_of_retirement, age_to_start_rmds, age_at_death,
                   roth_rollover_amount, income, yearly_income_raise,
                   max_income, age_of_marriage):
    """This function will print the state of each year depending on the inputs
    provided until you die.
    """

    assert current_age < age_at_death
    print(f"Settings: {traditional=:,.2f}, {roth=:,.2f}, {interest_rate=:.2f}, {yearly_contribution_traditional=:,.2f}")
    print(f"          {yearly_contribution_roth=:,.2f}, {years_until_transition_to_pretax_contributions=}")
    print(f"          {current_age=}, {age_of_retirement=} {age_to_start_rmds=}, {age_at_death=}, {roth_rollover_amount=:,.2f}")
    print(f"          {income=:,.2f}, {yearly_income_raise=:.2f}, {max_income=:,.2f} {age_of_marriage=}")
    print("")

    taxes = 0
    total_contributions_traditional = 0
    total_contributions_roth = 0
    total_taxes = 0

    #
    # Doesn't really help me, but y'all might already be married.
    #
    married = True if age_of_marriage <= current_age else False

    #
    # Iterate over each year in our life.
    #
    for year in range(age_at_death - current_age):
        #
        # Print some major life status updates.
        #
        if year == years_until_transition_to_pretax_contributions:
            if current_age < age_of_retirement:
                print("you're starting pretax contributions")

        if current_age == age_to_start_rmds:
            print("you have rmds now")

        if current_age == age_of_retirement:
            print("you're now retired, stopping contributions{}".format(
                ", doing roth rollovers" if roth_rollover_amount else ""
            ))

        if current_age == age_of_marriage:
            print("you're now married")
            married = True

        #
        # Alright, if we're still working, we can make a tax-advantaged
        # contribution of some type. This might include tax deductions.
        #
        tax_deductions = 0
        if current_age < age_of_retirement:
            #
            # We are still working.
            #
            total_contributions_roth += yearly_contribution_roth
            roth += yearly_contribution_roth

            if year >= years_until_transition_to_pretax_contributions:
                total_contributions_traditional += yearly_contribution_traditional
                traditional += yearly_contribution_traditional
                tax_deductions += yearly_contribution_traditional
            else:
                #
                # We are diverting traditional to roth.
                #
                total_contributions_roth += yearly_contribution_traditional
                roth += yearly_contribution_traditional
                
        else:
            #
            # We have retired.
            #
            roth_rollover_amount = min(traditional, roth_rollover_amount)
            income = roth_rollover_amount
            if roth_rollover_amount and current_age < age_to_start_rmds:
                roth += roth_rollover_amount
                traditional -= roth_rollover_amount

        #
        # Do we need to make RMDs?
        #
        if current_age >= age_to_start_rmds:
            rmd = traditional/withdrawal_factors[current_age]
            traditional -= rmd
            income = rmd
        else:
            rmd = 0

        #
        # How much taxes are we going to pay this year?
        #
        taxable_income = income - tax_deductions
        assert taxable_income > 0
        taxes = calculate_taxes(taxable_income, married)
        total_taxes += taxes

        #
        # Calculate the effective tax rate.
        #
        try:
            tax_rate = (taxes/income) * 100
        except ZeroDivisionError:
            tax_rate = 0

        print(f"{current_age=:3d} || {roth=:13,.2f} || {traditional=:13,.2f} || {rmd=:11,.2f} || {taxable_income=:10,.2f} || {taxes=:10,.2f} || {tax_rate=:5.2f} || {total_taxes=:12,.2f}")

        #
        # Happy new year! It's the end of the year. Apply interest, give
        # yourself a pay raise, and happy birthday!
        #
        traditional *= interest_rate
        roth *= interest_rate
        if current_age < age_of_retirement:
            income = income * yearly_income_raise
            if max_income:
                income = min(income, max_income)
        current_age += 1

    print("congrats, you're dead")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate RMDs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    #
    # Arguments without defaults.
    #
    parser.add_argument(
        "--current-age",
        help="Your current age",
        required=True,
        type=int
    )
    parser.add_argument(
        "--income",
        help="Your current income",
        required=True,
        type=float
    )

    #
    # Arguments with defaults.
    #
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
        default=19500
    )
    parser.add_argument(
        "--yearly-contribution-roth",
        help="How much are you contributing to Roth per year?",
        required=False,
        type=float,
        default=6000
    )
    parser.add_argument(
        "--years-until-transition-to-pretax-contributions",
        metavar="YEARS",
        required=False,
        type=int,
        default=5
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
        "--age-at-death",
        help="When do you plan on dying?",
        required=False,
        type=int,
        default=116
    )
    parser.add_argument(
        "--roth-rollover-amount",
        help="After retirement, how much will you rollover from Traditional -> Roth per year?",
        required=False,
        type=float,
        default=50000
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
        default=200
    )

    args = parser.parse_args()

    calculate_rmds(
        args.principal_traditional,
        args.principal_roth,
        args.interest_rate,
        args.yearly_contribution_traditional,
        args.yearly_contribution_roth,
        args.years_until_transition_to_pretax_contributions,
        args.current_age,
        args.age_of_retirement,
        args.age_to_start_rmds,
        args.age_at_death,
        args.roth_rollover_amount,
        args.income,
        args.yearly_income_raise,
        args.max_income,
        args.age_of_marriage
    )
