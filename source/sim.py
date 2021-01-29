#!/usr/bin/env python3
#
import argparse

from rich.table import Table
from rich.live import Live
from rich.console import Console

import federal_taxes
import state_taxes
import ult

from account import Account


class SimulationResults:
    """
    This is a container for all of the return values.
    """
    def __init__(self, assets, traditional, params_table, math_table,
                 summary_table, needed_to_continue):
        self.assets = assets
        self.traditional = traditional
        self.params_table = params_table
        self.math_table = math_table
        self.summary_table = summary_table
        self.needed_to_continue = needed_to_continue


def calculate_assets(
        starting_balance_taxable,
        starting_balance_trad_401k,
        starting_balance_trad_ira,
        starting_balance_roth_401k,
        starting_balance_roth_ira,
        rate_of_return,
        years_until_transition_to_pretax_contributions,
        current_age,
        age_of_retirement,
        age_to_start_rmds,
        age_of_death,
        roth_conversion_amount,
        income,
        yearly_income_raise,
        max_income,
        age_of_marriage,
        spending,
        yearly_401k_normal_contribution_limit,
        yearly_401k_total_contribution_limit,
        yearly_ira_contribution_limit,
        ira_contribution_catch_up,
        ira_contribution_catch_up_age,
        do_mega_backdoor_roth,
        work_state,
        retirement_state,
        dependents,
        public_safety_employee
    ):
    """Simulate the state of finances for every year until you die."""
    assert current_age <= 115
    assert age_of_death <= 115
    assert income >= 0
    if max_income:
        assert max_income >= income
    assert current_age < age_of_death
    assert yearly_401k_total_contribution_limit >= yearly_401k_normal_contribution_limit

    #
    # Input parameters:
    #
    params_table = Table(show_header=True, header_style="bold magenta")
    params_table.add_column("Field")
    params_table.add_column("Value", justify="right")
    params_table.add_row("Starting Age", str(current_age))
    params_table.add_row("Age of Death", str(age_of_death))
    params_table.add_row("Age of Marriage", str(age_of_marriage))
    params_table.add_row("Age of Retirement", str(age_of_retirement))
    params_table.add_row("Age to Start RMDs", str(age_to_start_rmds))
    params_table.add_row("Starting Income", f"{income:,.2f}")
    params_table.add_row("Max Income", f"{max_income:,.2f}" if max_income else None)
    params_table.add_row("Yearly Rate of Return", f"{(rate_of_return-1)*100:.2f}%")
    params_table.add_row("Yearly Income Raise", f"{(yearly_income_raise-1)*100:.2f}%")
    params_table.add_row("Starting Balance Taxable", f"{starting_balance_taxable:,.2f}")
    params_table.add_row("Starting Balance Trad 401k", f"{starting_balance_trad_401k:,.2f}")
    params_table.add_row("Starting Balance Trad IRA", f"{starting_balance_trad_ira:,.2f}")
    params_table.add_row("Starting Balance Roth 401k", f"{starting_balance_roth_401k:,.2f}")
    params_table.add_row("Starting Balance Roth IRA", f"{starting_balance_roth_ira:,.2f}")
    params_table.add_row("Yearly Roth Conversion Amount", f"{roth_conversion_amount:,.2f}")
    params_table.add_row("Years to Prefer Roth Contributions", str(years_until_transition_to_pretax_contributions))
    params_table.add_row("Yearly Spending", f"{spending:,.2f}")
    params_table.add_row("Yearly 401k Pre-tax Limit", f"{yearly_401k_normal_contribution_limit:,.2f}")
    params_table.add_row("Yearly 401k Contribution Limit", f"{yearly_401k_total_contribution_limit:,.2f}")
    params_table.add_row("Yearly IRA Contribution Limit", f"{yearly_ira_contribution_limit:,.2f}")
    params_table.add_row("Do Mega-Backdoor Roth After Tax-Advantaged Limit?", str(do_mega_backdoor_roth))
    params_table.add_row("Work State", work_state)
    params_table.add_row("Retirement State", retirement_state)

    #
    # These are life-time counters.
    #
    total_taxes = 0

    #
    # These are our accounts:
    #
    taxable_account = Account(
        name="Taxable",
        rate_of_return=rate_of_return,
        starting_balance=starting_balance_taxable,
        withdrawal_contributions_first=False
    )
    roth_401k = Account(
        name="Roth 401k",
        rate_of_return=rate_of_return,
        starting_balance=starting_balance_roth_401k,
        withdrawal_contributions_first=True
    )
    roth_ira = Account(
        name="Roth IRA",
        rate_of_return=rate_of_return,
        starting_balance=starting_balance_roth_ira,
        withdrawal_contributions_first=True
    )
    trad_401k = Account(
        name="Traditional 401k",
        rate_of_return=rate_of_return,
        starting_balance=starting_balance_trad_401k,
        withdrawal_contributions_first=False
    )
    trad_ira = Account(
        name="Traditional IRA",
        rate_of_return=rate_of_return,
        starting_balance=starting_balance_trad_ira,
        withdrawal_contributions_first=False
    )

    #
    # The initial values for life events.
    #
    married = age_of_marriage < current_age
    retired = False
    prefer_roth = True
    rule_of_55_age = 50 if public_safety_employee else 55

    def num_dependents(current_age):
        if dependents is None:
            return 0
        count = 0
        for dep in dependents:
            #
            # Taxpayers may be able to claim the child tax credit if they have a
            # qualifying child under the age of 17. Part of this credit can be
            # refundable, so it may give a taxpayer a refund even if they don't
            # owe any tax.
            #
            if dep <= current_age < (dep + 17):
                count += 1
        return count

    if married:
        yearly_ira_contribution_limit *= 2
    if current_age > ira_contribution_catch_up_age:
        yearly_ira_contribution_limit += ira_contribution_catch_up

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Age", justify="right")
    table.add_column("M", justify="center")
    table.add_column("R", justify="center")
    table.add_column("Roth 401k", justify="right")
    table.add_column("Diff", justify="right")
    table.add_column("Roth IRA", justify="right")
    table.add_column("Diff", justify="right")
    table.add_column("Taxable", justify="right")
    table.add_column("Diff", justify="right")
    table.add_column("Trad 401k", justify="right")
    table.add_column("Diff", justify="right")
    table.add_column("RMD", justify="right")
    table.add_column("Trad IRA", justify="right")
    table.add_column("Diff", justify="right")
    table.add_column("RMD", justify="right")
    table.add_column("MAGI", justify="right")
    table.add_column("Spending", justify="right")
    table.add_column("Deps", justify="center")
    table.add_column("State", justify="center")
    table.add_column("State Tax", justify="right")
    table.add_column("Penalties", justify="right")
    table.add_column("Federal Tax", justify="right")
    table.add_column("Total Taxes", justify="right")

    needed_to_continue = 0

    #
    # Iterate over each year in our life.
    #
    for year in range(age_of_death - current_age + 1):

        ########################################################################
        # Life Events
        ########################################################################

        if current_age == age_of_retirement:
            retired = True
        if current_age == age_of_marriage:
            married = True
            yearly_ira_contribution_limit *= 2
        if year >= years_until_transition_to_pretax_contributions:
            prefer_roth = False

        if current_age == ira_contribution_catch_up_age:
            yearly_ira_contribution_limit += ira_contribution_catch_up
            if married:
                yearly_ira_contribution_limit += ira_contribution_catch_up

        #
        # If we have a different state set.
        #
        current_state = retirement_state if retired else work_state

        ########################################################################
        # Retirement Contribution Calculations
        ########################################################################

        tax_deductions = 0
        this_years_income = 0

        taxable_contribution = 0
        roth_401k_contribution = 0
        roth_ira_contribution = 0
        trad_401k_contribution = 0
        trad_ira_contribution = 0

        #
        # Calculate how much tax advantaged space we have. This will be our total
        # contribution limit for this year.
        #
        tax_advantaged_space = yearly_ira_contribution_limit
        if do_mega_backdoor_roth:
            tax_advantaged_space += yearly_401k_total_contribution_limit
        else:
            tax_advantaged_space += yearly_401k_normal_contribution_limit

        #
        # These variables are used to binary search the maximum contribution.
        #
        minimum_contribution = 0
        total_contribution_limit = tax_advantaged_space
        maximum_contribution = tax_advantaged_space

        #
        # Alright, if we're still working, we can make some tax-advantaged
        # contributions. If there is a traditional contribution, it will lower
        # our taxes and, as a result, will allow us to contribute more! This is
        # why we must binary search the maximum contribution.
        #
        if current_age < age_of_retirement:
            this_years_income = income

            #
            # We'll break out of this once the ideal amount is found.
            #
            while True:
                taxable_contribution = 0
                roth_401k_contribution = 0
                roth_ira_contribution = 0
                trad_401k_contribution = 0
                trad_ira_contribution = 0

                #
                # Calculate 401k contribution.
                #
                if prefer_roth:
                    roth_401k_contribution += min(min(
                        this_years_income,
                        yearly_401k_normal_contribution_limit
                    ), total_contribution_limit)
                else:
                    trad_401k_contribution += min(min(
                        this_years_income,
                        yearly_401k_normal_contribution_limit
                    ), total_contribution_limit)

                #
                # Calculate IRA contribution. If there are no tax deductions for
                # the traditional IRA (because our income is too high) we might
                # as well contribute to Roth.
                #
                would_be_ira_contribution = min(
                    min(this_years_income, yearly_ira_contribution_limit),
                    total_contribution_limit - roth_401k_contribution -
                        trad_401k_contribution
                )

                would_be_agi_if_trad = (
                    this_years_income
                    - trad_401k_contribution
                    - would_be_ira_contribution
                )

                #
                # TODO: Maybe add a more granular approach, rather than an all
                # or nothing approach.
                #
                if prefer_roth or not federal_taxes.fully_tax_deductible_ira(
                        would_be_agi_if_trad, married):
                    roth_ira_contribution += would_be_ira_contribution
                else:
                    trad_ira_contribution += would_be_ira_contribution

                #
                # Calculate Mega-Backdoor Roth contribution, if applicable.
                #
                if do_mega_backdoor_roth:
                    after_tax_contribution = min(
                        min(this_years_income, yearly_401k_total_contribution_limit),
                        total_contribution_limit - roth_401k_contribution -
                            trad_401k_contribution - roth_ira_contribution -
                            trad_ira_contribution
                    )
                    roth_ira_contribution += after_tax_contribution

                tax_deductions = (
                    trad_401k_contribution
                    + trad_ira_contribution
                )

                #
                # We know about all of our tax deductions, we can accurately
                # calculate our taxes now.
                #
                taxable_income = this_years_income - tax_deductions
                fica_tax = federal_taxes.calculate_fica_tax(this_years_income, married)
                federal_income_tax = federal_taxes.calculate_federal_income_tax(
                    taxable_income,
                    married,
                    num_dependents(current_age)
                )
                federal_income_tax -= federal_taxes.calculate_savers_credit(
                    taxable_income,
                    (
                        roth_401k_contribution
                        + trad_401k_contribution
                        + roth_ira_contribution
                        + trad_ira_contribution
                    ),
                    married
                )
                state_tax = state_taxes.calculate_state_tax(
                    taxable_income,
                    married,
                    current_state,
                    num_dependents(current_age)
                )

                #
                # We can't have negative taxes. The saver's credit could
                # potentially be more than our total federal income tax.
                #
                federal_income_tax = max(federal_income_tax, 0)

                result = (
                    this_years_income
                    - spending
                    - fica_tax
                    - federal_income_tax
                    - state_tax
                    - roth_401k_contribution
                    - trad_401k_contribution
                    - roth_ira_contribution
                    - trad_ira_contribution
                )

                #
                # Binary search our way to the ideal contribution. We want the
                # result to be zero, which will happen when there is no leftover
                # money after taxes.
                #
                if result > 0:
                    if total_contribution_limit == tax_advantaged_space:
                        break
                    minimum_contribution = total_contribution_limit
                    total_contribution_limit = (
                        minimum_contribution
                        + maximum_contribution
                    )/2
                elif result < 0:
                    if total_contribution_limit == 0:
                        break
                    maximum_contribution = total_contribution_limit
                    total_contribution_limit = (
                        minimum_contribution
                        + maximum_contribution
                    )/2
                else:
                    break

            roth_401k.contribute(roth_401k_contribution)
            trad_401k.contribute(trad_401k_contribution)
            roth_ira.contribute(roth_ira_contribution)
            trad_ira.contribute(trad_ira_contribution)

        ########################################################################
        # Required Minimum Distribution (RMD) Calculations
        ########################################################################

        trad_401k_rmd = 0
        trad_ira_rmd = 0
        if current_age >= age_to_start_rmds:
            trad_401k_rmd = round(trad_401k.get_value()/ult.withdrawal_factors[current_age], 2)
            trad_ira_rmd = round(trad_ira.get_value()/ult.withdrawal_factors[current_age], 2)

        ########################################################################
        # Withdrawals
        ########################################################################

        total_assets = (
            taxable_account.get_value()
            + trad_ira.get_value()
            + trad_401k.get_value()
            + roth_ira.get_value()
            + roth_401k.get_value()
        )

        bare_minimum_withdrawal = trad_401k_rmd + trad_ira_rmd
        if retired and (current_age < age_to_start_rmds):
            bare_minimum_withdrawal += roth_conversion_amount
        minimum_withdrawal = bare_minimum_withdrawal
        total_withdrawal = bare_minimum_withdrawal
        maximum_withdrawal = total_assets
        penalty_fees = 0

        stop_simulation = False

        #
        # TODO: Order withdrawals based on situation.
        #
        while True:
            taxable_withdrawal = 0
            roth_401k_withdrawal = 0
            roth_ira_withdrawal = 0
            trad_401k_withdrawal = 0
            trad_ira_withdrawal = 0
            roth_401k_with_interest_withdrawal = 0
            roth_ira_with_interest_withdrawal = 0

            ltcg_taxes = 0
            penalty_fees = 0
            conversion_amount = 0
            roth_gains = 0
            savers_credit = 0

            def whats_left_to_withdrawal():
                return (
                    total_withdrawal
                    - taxable_withdrawal
                    - roth_401k_withdrawal
                    - roth_ira_withdrawal
                    - roth_401k_with_interest_withdrawal
                    - roth_ira_with_interest_withdrawal
                    - trad_401k_withdrawal
                    - trad_ira_withdrawal
                )

            #
            # First things first, take the RMDs.
            #
            trad_401k_withdrawal += trad_401k_rmd
            trad_ira_withdrawal += trad_ira_rmd

            #
            # Roth conversions. While we're retired, but before RMDs, let's do
            # some rollovers from our traditional to Roth accounts. This will
            # allow the money to grow tax free in Roth accounts.
            #
            # TODO: Be sure to enforce the 5 year maturity rule.
            #
            if retired and (current_age < age_to_start_rmds):
                trad_401k_conversion = min(
                    trad_401k.get_value() - trad_401k_withdrawal,
                    roth_conversion_amount
                )
                trad_ira_conversion = min(
                    trad_ira.get_value() - trad_ira_withdrawal,
                    roth_conversion_amount - trad_401k_conversion
                )

                conversion_amount = trad_401k_conversion + trad_ira_conversion
                trad_401k_withdrawal += trad_401k_conversion
                trad_ira_withdrawal += trad_ira_conversion

            #
            # If we can withdrawal money without penalty, we should at least
            # withdrawal the standard deduction, because this will not have
            # federal income taxes.
            #
            if (current_age >= rule_of_55_age >= age_of_retirement) or current_age >= 60:
                trad_401k_withdrawal += min(min(
                    trad_401k.get_value() - trad_401k_withdrawal,
                    max((
                        federal_taxes.get_standard_deduction(married)
                        - this_years_income
                        - trad_401k_withdrawal
                        - trad_ira_withdrawal
                    ), 0)
                ), whats_left_to_withdrawal())

            #
            # If we didn't get enough from the traditional 401k, the next best
            # option is taxable. Up until the $80k mark for married folk. This
            # is a lot of space.
            #
            # If we're younger than 60, we want to do this before we try to
            # withdrawal from IRAs, because those will be penalized.
            #
            if current_age < 60:
                taxable_withdrawal += min(min(
                    taxable_account.get_value() - taxable_withdrawal,
                    whats_left_to_withdrawal()
                ), max(federal_taxes.zero_tax_ltcg_income(married) - (
                        this_years_income
                        + trad_401k_withdrawal
                        + trad_ira_withdrawal
                        - tax_deductions
                    ), 0)
                )

            #
            # Next, if we didn't have enough in taxable, we should take from the
            # traditional IRA up to the standard deduction, so it's not taxed.
            #
            if current_age >= 60:
                trad_ira_withdrawal += min(min(
                    trad_ira.get_value() - trad_ira_withdrawal,
                    max((
                        federal_taxes.get_standard_deduction(married)
                        - this_years_income
                        - trad_401k_withdrawal
                        - trad_ira_withdrawal
                    ), 0)
                ), whats_left_to_withdrawal())

            #
            # This will withdrawal whatever we need from the LTCG zero bracket
            # regardless of age.
            #
            taxable_withdrawal += min(min(
                taxable_account.get_value() - taxable_withdrawal,
                whats_left_to_withdrawal()
            ), max(federal_taxes.zero_tax_ltcg_income(married) - (
                    this_years_income
                    + trad_401k_withdrawal
                    + trad_ira_withdrawal
                    - tax_deductions
                ), 0)
            )

            #
            # Next, regardless of penalty, take the standard deduction.
            #
            trad_401k_withdrawal += min(min(
                trad_401k.get_value() - trad_401k_withdrawal,
                max((
                    federal_taxes.get_standard_deduction(married)
                    - this_years_income
                    - trad_401k_withdrawal
                    - trad_ira_withdrawal
                ), 0)
            ), whats_left_to_withdrawal())

            #
            # If the trad 401k runs out of money, this will cover the rest.
            #
            trad_ira_withdrawal += min(min(
                trad_ira.get_value() - trad_ira_withdrawal,
                max((
                    federal_taxes.get_standard_deduction(married)
                    - this_years_income
                    - trad_401k_withdrawal
                    - trad_ira_withdrawal
                ), 0)
            ), whats_left_to_withdrawal())

            #
            # This will be penalty free.
            #
            roth_401k_withdrawal += min(
                roth_401k.get_contributions() - roth_401k_withdrawal,
                whats_left_to_withdrawal()
            )
            roth_ira_withdrawal += min(
                roth_ira.get_contributions() - roth_ira_withdrawal,
                whats_left_to_withdrawal()
            )

            #
            # Time to drain our taxable account. Everything else will cost us.
            # LTCG will be cheaper than income tax.
            #
            taxable_withdrawal += min(
                taxable_account.get_value() - taxable_withdrawal,
                whats_left_to_withdrawal()
            )

            #
            # We'll have to pay some level of income tax on this.
            #
            trad_401k_withdrawal += min(
                trad_401k.get_value() - trad_401k_withdrawal,
                whats_left_to_withdrawal()
            )
            trad_ira_withdrawal += min(
                trad_ira.get_value() - trad_ira_withdrawal,
                whats_left_to_withdrawal()
            )

            #
            # Unless we're younger than 60, we'll have to pay income tax on the
            # gains. If we're this far, that means we have already extracted all
            # of our contributions, meaning this whole thing will be treated as
            # income.
            #
            roth_401k_with_interest_withdrawal += min(
                roth_401k.get_value() - roth_401k_withdrawal,
                whats_left_to_withdrawal()
            )
            roth_ira_with_interest_withdrawal += min(
                roth_ira.get_value() - roth_ira_withdrawal,
                whats_left_to_withdrawal()
            )

            #
            # Police officers, firefighters, EMTs, and air traffic controllers
            # are considered public safety employees, and they get a little
            # extra time to access their qualified retirement plans. For them,
            # the rule applies in the calendar year in which they turn 50.
            #
            # TODO: Check that these are right.
            #
            rule_of_55_age = 50 if public_safety_employee else 55
            if current_age < 60:
                penalty_fees += roth_ira_withdrawal * 0.10
                penalty_fees += trad_ira_withdrawal * 0.10
            if current_age < 60:
                if not current_age >= rule_of_55_age >= age_of_retirement:
                    penalty_fees += roth_401k_withdrawal * 0.10
                    penalty_fees += trad_401k_withdrawal * 0.10

            #
            # If you’re over 59½ and your account is at least five years old,
            # you can withdraw contributions and earnings with no tax or
            # penalty. We don't support half ages.
            #
            if current_age < 60:
                roth_gains += roth_401k.withdrawal(
                    roth_401k_with_interest_withdrawal,
                    dry_run=True
                ).get_gains()
                roth_gains += roth_ira.withdrawal(
                    roth_ira_with_interest_withdrawal,
                    dry_run=True
                ).get_gains()

            taxable_income = round(
                this_years_income
                + trad_401k_withdrawal
                + trad_ira_withdrawal
                + roth_gains
                - tax_deductions,
                2
            )

            #
            # Now that we know our taxable income, we can calculate LTCG tax.
            #
            if taxable_withdrawal:
                withdrawal = taxable_account.withdrawal(
                    taxable_withdrawal,
                    dry_run=True
                )
                ltcg_taxes = federal_taxes.calculate_federal_income_tax(
                    taxable_income, married, ltcg=withdrawal.get_gains(),
                    just_ltcg=True
                )

            #
            # When calculating the FICA tax, we must not include retirement
            # distributions. These have already been taxed by FICA.
            #
            fica_tax = federal_taxes.calculate_fica_tax(
                max(this_years_income, 0),
                married
            )

            #
            # Calculate the federal taxes. This includes the federal income tax
            # and FICA (social security and medicare) tax.
            #
            federal_income_tax = federal_taxes.calculate_federal_income_tax(
                taxable_income,
                married,
                num_dependents(current_age)
            )

            #
            # Calculate saver's credit. This provides tax credits if you are low
            # income and made retirement contributions.
            #
            if not retired:
                savers_credit = federal_taxes.calculate_savers_credit(
                    taxable_income,
                    (
                        roth_401k_contribution
                        + roth_ira_contribution
                        + trad_401k_contribution
                        + trad_ira_contribution
                    ),
                    married
                )

            #
            # Apply saver's credit. Credits cannot result in negative taxes.
            #
            federal_income_tax = max(federal_income_tax - savers_credit, 0)

            #
            # Finally, calculate state taxes, if any.
            #
            state_tax = state_taxes.calculate_state_tax(
                taxable_income,
                married,
                current_state,
                num_dependents(current_age)
            )

            this_years_taxes = (
                federal_income_tax
                + fica_tax
                + state_tax
                + ltcg_taxes
            )

            #
            # This boils down to income minus expenses.
            #
            result = (
                this_years_income
                - this_years_taxes
                - spending
                - taxable_contribution
                - roth_401k_contribution
                - roth_ira_contribution
                - trad_401k_contribution
                - trad_ira_contribution
                - conversion_amount
                - penalty_fees
                + taxable_withdrawal
                + roth_401k_withdrawal
                + roth_ira_withdrawal
                + roth_401k_with_interest_withdrawal
                + roth_ira_with_interest_withdrawal
                + trad_401k_withdrawal
                + trad_ira_withdrawal
            )

            #
            # We've calculated the result (excess/insufficent funds).
            #
            # If we have excess money, lower the withdrawal until we withdrawal
            # is nothing. If there's still money leftover then, put it in a
            # taxable account.
            #
            # If we have insufficent money, raise the withdrawal until we've
            # reached our total assets. If we are withdrawaling all of our
            # assets and we still need money, we need to stop the simulation.
            #
            if round(result, 2) > 0:
                #
                # We have excess money.
                #
                if round(total_withdrawal, 2) == round(bare_minimum_withdrawal, 2):
                    taxable_contribution = result
                    taxable_account.contribute(taxable_contribution)
                    break
                maximum_withdrawal = total_withdrawal
                total_withdrawal = (
                    minimum_withdrawal
                    + maximum_withdrawal
                )/2
            elif round(result, 2) < 0:
                #
                # We need money.
                #
                if round(total_withdrawal, 2) == round(total_assets, 2):
                    needed_to_continue = abs(result)
                    stop_simulation = True
                    break
                minimum_withdrawal = total_withdrawal
                total_withdrawal = (
                    minimum_withdrawal
                    + maximum_withdrawal
                )/2
            else:
                break

        withdrawals = [
            roth_401k.withdrawal(roth_401k_withdrawal),
            roth_401k.withdrawal(roth_401k_with_interest_withdrawal),
            trad_401k.withdrawal(trad_401k_withdrawal),
            roth_ira.withdrawal(roth_ira_withdrawal),
            roth_ira.withdrawal(roth_ira_with_interest_withdrawal),
            trad_ira.withdrawal(trad_ira_withdrawal),
            taxable_account.withdrawal(taxable_withdrawal)
        ]
        for withdrawal in withdrawals:
            assert withdrawal.get_insufficient() == 0, withdrawal

        #
        # Now is the time to do the Roth conversion.
        #
        roth_ira_contribution += conversion_amount
        roth_ira.contribute(conversion_amount, rollover=True)

        #
        # Now that we've finalized our withdrawals, we know our taxes.
        #
        total_taxes += this_years_taxes

        ########################################################################
        # Data Collection
        ########################################################################

        this_years_federal_taxes = federal_income_tax + fica_tax

        #
        # We have finished the year. Add an entry to the table. This will get
        # printed when the simulation is over.
        #
        table.add_row(
            f"{current_age}",
            ":heart_eyes:" if married else "",
            ":tada:" if retired else "",
            f"{roth_401k.get_value():,.2f}",
            f"{roth_401k.get_yearly_diff()}",
            f"{roth_ira.get_value():,.2f}",
            f"{roth_ira.get_yearly_diff()}",
            f"{taxable_account.get_value():,.2f}",
            f"{taxable_account.get_yearly_diff()}",
            f"{trad_401k.get_value():,.2f}",
            f"{trad_401k.get_yearly_diff()}",
            f"[yellow]{trad_401k_rmd:,.2f}[/yellow]" if trad_401k_rmd else "",
            f"{trad_ira.get_value():,.2f}",
            f"{trad_ira.get_yearly_diff()}",
            f"[yellow]{trad_ira_rmd:,.2f}[/yellow]" if trad_ira_rmd else "",
            f"[cyan]{taxable_income:,.2f}[/cyan]",
            f"[red]{spending:,.2f}[/red]",
            f"{num_dependents(current_age):d}",
            f"{current_state}",
            f"[red]{state_tax:,.2f}[/red]" if round(state_tax, 2) else "",
            f"[red]{penalty_fees:,.2f}[/red]" if round(penalty_fees, 2) else "",
            f"[red]{this_years_federal_taxes:,.2f}[/red]" if round(this_years_federal_taxes, 2) else "",
            f"[purple]{total_taxes:,.2f}[/purple]",
        )

        if stop_simulation:
            break

        ########################################################################
        # Preparation for New Year
        ########################################################################

        #
        # Happy new year! It's the end of the year. Apply return, give
        # yourself a pay raise, and happy birthday!
        #
        current_age += 1
        if current_age > age_of_death:
            break

        taxable_account.increment()
        roth_401k.increment()
        roth_ira.increment()
        trad_401k.increment()
        trad_ira.increment()

        if current_age < age_of_retirement:
            income *= yearly_income_raise
            if max_income:
                income = min(income, max_income)

    #
    # Do not sell stocks before death. They get a "step up in basis" meaning the
    # basis changes. The heir will only be responsible for gains after
    # inheritance.
    #
    total_assets = (
        taxable_account.get_value()
        + trad_ira.get_value()
        + trad_401k.get_value()
        + roth_ira.get_value()
        + roth_401k.get_value()
    )

    estate_tax = federal_taxes.calculate_estate_tax(total_assets)

    #
    # This calculates the minimum tax your heir will be expected to pay as a
    # result of RMDs. This assumes they have no income.
    #
    # TODO: If the user specifies a dependent, use that to determine the
    # difference in age, rather than a hardcoded value. To simplify our
    # calculation, we can assume everything goes to the eldest child.
    #
    taxes_for_heir = federal_taxes.calculate_minimum_remaining_tax_for_heir(
        trad_401k.get_value() + trad_ira.get_value(),
        age_of_death - 30
    )

    death_tax = estate_tax + taxes_for_heir
    total_taxes += death_tax

    try:
        tax_to_asset_ratio = total_taxes/round(total_assets, 2)
    except ZeroDivisionError:
        tax_to_asset_ratio = None

    #
    # Print a summary of things.
    #
    summary_table = Table(show_header=True, header_style="bold magenta")
    summary_table.add_column("Field")
    summary_table.add_column("Value at Death", justify="right")
    summary_table.add_row("Taxable", f"{taxable_account.get_value():,.2f}")
    summary_table.add_row("Trad 401k", f"{trad_401k.get_value():,.2f}")
    summary_table.add_row("Trad IRA", f"{trad_ira.get_value():,.2f}")
    summary_table.add_row("Roth 401k", f"{roth_401k.get_value():,.2f}")
    summary_table.add_row("Roth IRA", f"{roth_ira.get_value():,.2f}")
    summary_table.add_row("Min Tax for Heir", f"{taxes_for_heir:,.2f}")
    summary_table.add_row("Estate Taxes", f"{estate_tax:,.2f}")
    summary_table.add_row("Total Taxes", f"{total_taxes:,.2f}")
    summary_table.add_row("Total Assets", f"{total_assets:,.2f}")
    summary_table.add_row("Total Assets After Taxes", f"{max(total_assets - death_tax, 0):,.2f}")
    summary_table.add_row("Tax/Asset Ratio", f"{tax_to_asset_ratio:,.2f}" if tax_to_asset_ratio else "")

    return SimulationResults(
        total_assets - death_tax,
        trad_401k.get_value() + trad_ira.get_value(),
        params_table,
        table,
        summary_table,
        needed_to_continue
    )


def main():
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
        "--starting-balance-taxable",
        help="Starting balance for taxable account?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--starting-balance-trad-401k",
        help="Starting balance for traditional 401k?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--starting-balance-trad-ira",
        help="Starting balance for traditional IRA?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--starting-balance-roth-401k",
        help="Starting balance for Roth 401k?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--starting-balance-roth-ira",
        help="Starting balance for Roth IRA?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--rate-of-return",
        help="What is the long-term rate of return?",
        required=False,
        type=float,
        default=1.04
    )
    parser.add_argument(
        "--yearly-401k-normal-contribution-limit",
        help="What is the normal 401k contribution limit?",
        required=False,
        type=float,
        default=19500
    )
    parser.add_argument(
        "--yearly-401k-total-contribution-limit",
        help="What is the total 401k contribution limit?",
        required=False,
        type=float,
        default=58000
    )
    parser.add_argument(
        "--yearly-ira-contribution-limit",
        help="What is the IRA contribution limit?",
        required=False,
        type=float,
        default=6000
    )
    parser.add_argument(
        "--ira-contribution-catch-up",
        help="How much extra can you contribute at this age?",
        required=False,
        type=float,
        default=1000
    )
    parser.add_argument(
        "--ira-contribution-catch-up-age",
        help="At what age can you do extra catch up contributions?",
        required=False,
        type=int,
        default=50
    )
    parser.add_argument(
        "--do-mega-backdoor-roth",
        help="What is the IRA contribution limit?",
        required=False,
        action='store_true',
        default=False
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
        "--work-state",
        help="What state will you work in?",
        required=False,
        choices=state_taxes.states.keys(),
        default='TX'
    )
    parser.add_argument(
        "--retirement-state",
        help="What state will you retire in?",
        required=False,
        choices=state_taxes.states.keys(),
        default='TX'
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
        "--spending",
        help="How much do you spend each year?",
        required=False,
        type=float,
        default=30000
    )
    parser.add_argument(
        "--add-dependent",
        help="Your age when dependent is to be added. This option can be used multiple times.",
        required=False,
        type=int,
        metavar="AGE",
        action='append'
    )
    parser.add_argument(
        "--public-safety-employee",
        help="Are you a public safety employee?",
        required=False,
        action='store_true',
        default=False
    )
    parser.add_argument(
        "--roth-conversion-unit",
        help="To what level of detail do you want to calculate the best Roth conversion?",
        required=False,
        type=float,
        default=1000
    )
    parser.add_argument(
        "--show-params",
        help="Show the parameters table.",
        action="store_true"
    )
    parser.add_argument(
        "--show-math",
        help="Show the calculation table.",
        action="store_true"
    )
    parser.add_argument(
        "--show-summary",
        help="Show the summary table.",
        action="store_true"
    )

    args = parser.parse_args()

    #
    # Calculate the most efficient Roth conversion amount.
    #
    most_assets = 0
    roth_conversion_amount = 0
    best_roth_conversion_amount = 0

    if not args.age_of_death > args.age_of_retirement:
        print("Retirement cannot be after death")
        return

    try:
        with Live(transient=True, refresh_per_second=144) as live:
            while True:
                results = calculate_assets(
                    args.starting_balance_taxable,
                    args.starting_balance_trad_401k,
                    args.starting_balance_trad_ira,
                    args.starting_balance_roth_401k,
                    args.starting_balance_roth_ira,
                    args.rate_of_return,
                    args.years_to_wait,
                    args.current_age,
                    args.age_of_retirement,
                    args.age_to_start_rmds,
                    args.age_of_death,
                    roth_conversion_amount, # this is our variable
                    args.income,
                    args.yearly_income_raise,
                    args.max_income,
                    args.age_of_marriage,
                    args.spending,
                    args.yearly_401k_normal_contribution_limit,
                    args.yearly_401k_total_contribution_limit,
                    args.yearly_ira_contribution_limit,
                    args.ira_contribution_catch_up,
                    args.ira_contribution_catch_up_age,
                    args.do_mega_backdoor_roth,
                    args.work_state,
                    args.retirement_state,
                    args.add_dependent,
                    args.public_safety_employee
                )
                live.update("Simulating with Roth conversion: "
                            f"{roth_conversion_amount:,.2f}")
                if round(results.assets, 2) >= round(most_assets, 2):
                    best_roth_conversion_amount = roth_conversion_amount
                    most_assets = results.assets
                if round(results.traditional, 2) == 0:
                    break
                roth_conversion_amount += args.roth_conversion_unit

        #
        # Now that we know all of the variables, run the simulation.
        #
        results = calculate_assets(
            args.starting_balance_taxable,
            args.starting_balance_trad_401k,
            args.starting_balance_trad_ira,
            args.starting_balance_roth_401k,
            args.starting_balance_roth_ira,
            args.rate_of_return,
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
            args.spending,
            args.yearly_401k_normal_contribution_limit,
            args.yearly_401k_total_contribution_limit,
            args.yearly_ira_contribution_limit,
            args.ira_contribution_catch_up,
            args.ira_contribution_catch_up_age,
            args.do_mega_backdoor_roth,
            args.work_state,
            args.retirement_state,
            args.add_dependent,
            args.public_safety_employee,
        )
    except KeyboardInterrupt:
        return

    #
    # Print stuff to the console if the user wants it.
    #
    console = Console()
    if args.show_params:
        console.print(results.params_table)
    if args.show_math:
        console.print(results.math_table)
    if args.show_summary:
        console.print(results.summary_table)

    #
    # If the user didn't specify to show anything, print the math table.
    #
    if not any([args.show_params, args.show_math, args.show_summary]):
        console.print(results.math_table)

    if results.needed_to_continue:
        console.print(":fire::fire::fire: Please enter "
                      f"[underline]{needed_to_continue:,.2f}[/underline]"
                      " to continue playing. :fire::fire::fire:")

if __name__ == "__main__":
    main()
