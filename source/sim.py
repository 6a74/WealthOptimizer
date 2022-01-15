#!/usr/bin/env python3

import argparse

from rich.table import Table
from rich.live import Live
from rich.console import Console

import federal_taxes
import state_taxes
import ult

from account import Account


class Simulation:
    """
    Simulate the state of finances for every year until you die.
    """

    def __init__(self,
                 starting_balance_hsa,
                 starting_balance_taxable,
                 starting_balance_trad_401k,
                 starting_balance_trad_ira,
                 starting_balance_roth_401k,
                 starting_balance_roth_ira,
                 rate_of_return,
                 years_to_wait,
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
                 contribution_limit_hsa,
                 contribution_catch_up_amount_hsa,
                 contribution_catch_up_age_hsa,
                 contribution_limit_401k,
                 contribution_limit_401k_total,
                 contribution_catch_up_amount_401k,
                 contribution_catch_up_age_401k,
                 contribution_limit_ira,
                 contribution_catch_up_amount_ira,
                 contribution_catch_up_age_ira,
                 mega_backdoor_roth,
                 work_state,
                 retirement_state,
                 dependents,
                 public_safety_employee,
                 employer_match_401k,
                 max_contribution_percentage_401k,
                 employer_contribution_hsa
    ):
        assert 0 <= current_age <= age_of_death <= 115
        assert 0 <= income
        if max_income:
            assert income <= max_income
        assert 0 <= contribution_limit_401k <= contribution_limit_401k_total
        assert 0 <= employer_match_401k <= 1.0
        assert 0 <= max_contribution_percentage_401k <= 1.0
        assert 0 <= employer_match_401k <= max_contribution_percentage_401k <= 1.0
        assert 0 <= employer_contribution_hsa <= contribution_limit_hsa

        #
        # Input parameters:
        #
        self.params_table = Table(show_header=True, header_style="bold magenta")
        self.params_table.add_column("Field")
        self.params_table.add_column("Value", justify="right")
        self.params_table.add_row("Starting Age", str(current_age))
        self.params_table.add_row("Age of Death", str(age_of_death))
        self.params_table.add_row("Age of Marriage", str(age_of_marriage))
        self.params_table.add_row("Age of Retirement", str(age_of_retirement))
        self.params_table.add_row("Age to Start RMDs", str(age_to_start_rmds))
        self.params_table.add_row("Starting Income", f"{income:,.2f}")
        self.params_table.add_row("Max Income", f"{max_income:,.2f}" if max_income else None)
        self.params_table.add_row("Yearly Rate of Return", f"{(rate_of_return-1)*100:.2f}%")
        self.params_table.add_row("Yearly Income Raise", f"{(yearly_income_raise-1)*100:.2f}%")
        self.params_table.add_row("Starting Balance Taxable", f"{starting_balance_taxable:,.2f}")
        self.params_table.add_row("Starting Balance HSA", f"{starting_balance_hsa:,.2f}")
        self.params_table.add_row("Starting Balance Trad 401k", f"{starting_balance_trad_401k:,.2f}")
        self.params_table.add_row("Starting Balance Trad IRA", f"{starting_balance_trad_ira:,.2f}")
        self.params_table.add_row("Starting Balance Roth 401k", f"{starting_balance_roth_401k:,.2f}")
        self.params_table.add_row("Starting Balance Roth IRA", f"{starting_balance_roth_ira:,.2f}")
        self.params_table.add_row("Yearly Roth Conversion Amount", f"{roth_conversion_amount:,.2f}")
        self.params_table.add_row("Years to Prefer Roth Contributions", str(years_to_wait))
        self.params_table.add_row("Spending", f"{spending:,.2f}")
        self.params_table.add_row("HSA Contribution Limit", f"{contribution_limit_hsa:,.2f}")
        self.params_table.add_row("HSA Catch-up Contribution", f"{contribution_catch_up_amount_hsa:,.2f}")
        self.params_table.add_row("HSA Catch-up Contribution Age", f"{contribution_catch_up_age_hsa:d}")
        self.params_table.add_row("401k Normal Contribution Limit", f"{contribution_limit_401k:,.2f}")
        self.params_table.add_row("401k Total Contribution Limit", f"{contribution_limit_401k_total:,.2f}")
        self.params_table.add_row("IRA Contribution Limit", f"{contribution_limit_ira:,.2f}")
        self.params_table.add_row("IRA Catch-up Contribution", f"{contribution_catch_up_amount_ira:,.2f}")
        self.params_table.add_row("IRA Catch-up Contribution Age", f"{contribution_catch_up_age_ira:d}")
        self.params_table.add_row("Do Mega-Backdoor Roth After Tax-Advantaged Limit?", str(mega_backdoor_roth))
        self.params_table.add_row("Work State", work_state)
        self.params_table.add_row("Retirement State", retirement_state)
        self.params_table.add_row("Employer Match 401k", f"{employer_match_401k*100:.2f}%")
        self.params_table.add_row("Max Contribution Percentage 401k", f"{max_contribution_percentage_401k*100:.2f}%")
        self.params_table.add_row("Employer Contribution HSA", f"{employer_contribution_hsa:,.2f}")

        class Accounts:
            """This class is just used as a container."""

        #
        # These are our accounts:
        #
        self.accounts = Accounts()
        self.accounts.hsa = Account(
            name="HSA",
            rate_of_return=rate_of_return,
            starting_balance=starting_balance_hsa,
            withdrawal_contributions_first=False
        )
        self.accounts.taxable = Account(
            name="Taxable",
            rate_of_return=rate_of_return,
            starting_balance=starting_balance_taxable,
            withdrawal_contributions_first=False
        )
        self.accounts.roth_401k = Account(
            name="Roth 401k",
            rate_of_return=rate_of_return,
            starting_balance=starting_balance_roth_401k,
            withdrawal_contributions_first=True
        )
        self.accounts.roth_ira = Account(
            name="Roth IRA",
            rate_of_return=rate_of_return,
            starting_balance=starting_balance_roth_ira,
            withdrawal_contributions_first=True
        )
        self.accounts.trad_401k = Account(
            name="Traditional 401k",
            rate_of_return=rate_of_return,
            starting_balance=starting_balance_trad_401k,
            withdrawal_contributions_first=False
        )
        self.accounts.trad_ira = Account(
            name="Traditional IRA",
            rate_of_return=rate_of_return,
            starting_balance=starting_balance_trad_ira,
            withdrawal_contributions_first=False
        )

        #
        # Static variables:
        #
        self.age_of_death = age_of_death
        self.age_of_marriage = age_of_marriage
        self.age_of_retirement = age_of_retirement
        self.age_to_start_rmds = age_to_start_rmds
        self.dependents = dependents
        self.max_income = max_income
        self.mega_backdoor_roth = mega_backdoor_roth
        self.public_safety_employee = public_safety_employee
        self.retirement_state = retirement_state
        self.roth_conversion_amount = roth_conversion_amount
        self.spending = spending
        self.starting_age = current_age
        self.starting_income = income
        self.work_state = work_state
        self.yearly_income_raise = yearly_income_raise
        self.years_to_wait = years_to_wait

        #
        # Dynamic variables:
        #
        self.year = 0
        self.total_taxes = 0
        self.needed_to_continue = 0

        #
        # Contribution limits:
        #
        self.contribution_limit_hsa = contribution_limit_hsa
        self.contribution_catch_up_amount_hsa = contribution_catch_up_amount_hsa
        self.contribution_catch_up_age_hsa = contribution_catch_up_age_hsa
        self.contribution_limit_401k = contribution_limit_401k
        self.contribution_limit_401k_total = contribution_limit_401k_total
        self.contribution_catch_up_amount_401k = contribution_catch_up_amount_401k
        self.contribution_catch_up_age_401k = contribution_catch_up_age_401k
        self.contribution_limit_ira = contribution_limit_ira
        self.contribution_catch_up_amount_ira = contribution_catch_up_amount_ira
        self.contribution_catch_up_age_ira = contribution_catch_up_age_ira
        self.employer_match_401k = employer_match_401k
        self.max_contribution_percentage_401k = max_contribution_percentage_401k
        self.employer_contribution_hsa = employer_contribution_hsa

        #
        # This will contain a table with all of our math.
        #
        self.table = Table(show_header=True, header_style="bold magenta")
        self.table.add_column("Age", justify="right")
        self.table.add_column("M", justify="center")
        self.table.add_column("R", justify="center")
        self.table.add_column("HSA", justify="right")
        self.table.add_column("Change", justify="right")
        self.table.add_column("Roth 401k", justify="right")
        self.table.add_column("Change", justify="right")
        self.table.add_column("Roth IRA", justify="right")
        self.table.add_column("Change", justify="right")
        self.table.add_column("Taxable", justify="right")
        self.table.add_column("Change", justify="right")
        self.table.add_column("Trad 401k", justify="right")
        self.table.add_column("Change", justify="right")
        self.table.add_column("RMD", justify="right")
        self.table.add_column("Trad IRA", justify="right")
        self.table.add_column("Change", justify="right")
        self.table.add_column("RMD", justify="right")
        self.table.add_column("Income", justify="right")
        self.table.add_column("Spending", justify="right")
        self.table.add_column("Deps", justify="center")
        self.table.add_column("State", justify="center")
        self.table.add_column("State Tax", justify="right")
        self.table.add_column("Penalties", justify="right")
        self.table.add_column("Federal Tax", justify="right")
        self.table.add_column("Total Taxes", justify="right")

    def get_needed_to_continue(self):
        """
        During the simulation, if you run out of money, this variable will be
        set to a positive value. If this variable is zero when the simulation is
        complete, that means you died with money remaining. This is ideal. But
        if this variable is non-zero, that means you were unable to meet your
        financial obligations.
        """
        return self.needed_to_continue

    def stop_simulation(self):
        """
        We should stop the simulation if we run out of money or we are dead.
        """
        if self.get_needed_to_continue():
            return True
        return not self.is_alive()

    def get_simulation_year(self):
        """
        This is the current year in the simulation. This will range between zero
        and (age of death - starting age).
        """
        return self.year

    def is_alive(self):
        return self.get_current_age() < self.age_of_death

    def get_current_age(self):
        return self.starting_age + self.year

    def is_married(self):
        return self.get_current_age() >= self.age_of_marriage

    def get_age_of_retirement(self):
        return self.age_of_retirement

    def is_retired(self):
        return self.get_current_age() >= self.get_age_of_retirement()

    def get_current_state(self):
        return self.retirement_state if self.is_retired() else self.work_state

    def get_income(self):
        """
        This is calculated based on what the simulation year is. If you have a
        yearly income raise, your income will be compounded until it hits the
        income ceiling.
        """
        if self.is_retired():
            return 0
        multiplier = self.yearly_income_raise ** self.get_simulation_year()
        return max(self.starting_income * multiplier, self.max_income)

    def get_spending(self):
        return self.spending

    def get_rule_of_55_age(self):
        """
        Under the terms of this rule, you can withdraw funds from your current
        job’s 401(k) or 403(b) plan with no 10% tax penalty if you leave that
        job in or after the year you turn 55. (Qualified public safety workers
        can start even earlier, at 50.) It doesn’t matter whether you were laid
        off, fired, or just quit.

        https://smartasset.com/retirement/401k-55-rule
        """
        return 50 if self.public_safety_employee else 55

    def can_make_401k_withdrawal_penalty_free(self):
        """
        Check if we can withdrawal without penalty. This depends on how old we
        are, when we retired, and what our profession is.
        """
        if self.get_current_age() >= 60:
            return True
        if self.is_retired():
            if self.age_of_retirement >= self.get_rule_of_55_age():
                return True
        return False

    def can_make_hsa_withdrawal_penalty_free(self):
        """
        There is no additional tax on distributions made after the date you are
        disabled, reach age 65, or die.

        https://www.fidelity.com/viewpoints/wealth-management/hsas-and-your-retirement
        """
        return self.get_current_age() >= 65

    def can_make_ira_withdrawal_penalty_free(self):
        """
        IRA withdrawal rules are pretty simple. There are no exceptions that I
        am aware of.
        """
        return self.get_current_age() >= 60

    def roth_gains_are_taxable(self):
        """
        You can withdrawal Roth contributions at anytime without penalty, but
        you cannot always withdraw the gains. Like IRA rules, this is pretty
        simple. There are no exceptions to this.
        """
        return self.get_current_age() < 60

    def prefer_roth(self):
        """
        The "years to wait" variable is how many years we wait until start to
        prefer traditional contributions. This is a bit confusing, I'm sorry.
        """
        return self.years_to_wait > self.get_simulation_year()

    def must_take_rmds(self):
        return self.get_current_age() >= self.age_to_start_rmds

    def get_rmd(self, value):
        return round(value/ult.withdrawal_factors[self.get_current_age()], 2)

    def get_num_dependents(self):
        """
        The dependents variable is a list of ages that you introduce a new
        dependent (presumably a child) into your life. We assume that these
        people are only dependents for 16 years. There are many rules and
        exceptions to this, so I apoligize for simplifying it too much.
        """
        if self.dependents is None:
            return 0
        count = 0
        for dep in self.dependents:
            #
            # Taxpayers may be able to claim the child tax credit if they have a
            # qualifying child under the age of 17. Part of this credit can be
            # refundable, so it may give a taxpayer a refund even if they don't
            # owe any tax.
            #
            if dep <= self.get_current_age() < (dep + 17):
                count += 1
        return count

    def get_hsa_contribution_limit(self):
        """
        In any case, the IRS treats married couples as a single tax unit, which
        means they must share one family HSA contribution limit of $7,200. In
        cases where both spouses have self-only coverage, each spouse may
        contribute up to $3,600 each year in separate accounts.

        If both spouses are 55 or older and not enrolled in Medicare, each
        spouse’s contribution limit is increased by the additional contribution.
        If both spouses meet the age requirement, the total contributions under
        family coverage can’t be more than $9,200. Each spouse must make the
        additional contribution to his or her own HSA. So let's assume if you're
        married you have separate HSA accounts and know you can do this.
        """
        limit = self.contribution_limit_hsa
        if self.get_current_age() >= self.contribution_catch_up_age_hsa:
            limit += self.contribution_catch_up_amount_hsa
        if self.is_married():
            limit *= 2
        return limit

    def get_ira_contribution_limit(self):
        """
        The IRA contribution limit variable should be per person. This function
        will calculate any exceptions based on your age or marriage.
        """
        limit = self.contribution_limit_ira
        if self.get_current_age() >= self.contribution_catch_up_age_ira:
            limit += self.contribution_catch_up_amount_ira
        if self.is_married():
            limit *= 2
        return limit

    def get_401k_normal_contribution_limit(self):
        """
        This is the "normal" contribution limit for traditional/Roth 401k's. It
        is not the total employee + employer contribution limit. That is the
        following function.
        """
        limit = self.contribution_limit_401k
        if self.get_current_age() >= self.contribution_catch_up_age_401k:
            limit += self.contribution_catch_up_amount_401k
        return limit

    def get_401k_total_contribution_limit(self):
        """
        For employees in 2021, the total contributions to all 401(k) accounts
        held by the same employee (regardless of current employment status) is
        $58,000, or 100% of compensation, whichever is less.
        """
        return min(self.contribution_limit_401k_total, self.get_income())

    def do_mega_backdoor_roth(self):
        return self.mega_backdoor_roth

    def get_tax_advantaged_space(self):
        """
        This calculates the total tax advantaged space that you have during the
        current simulation year. It includes 401k and IRA contributions.
        """
        space = self.get_ira_contribution_limit()
        space += self.get_hsa_contribution_limit()
        if self.do_mega_backdoor_roth():
            space += self.get_401k_total_contribution_limit()
        else:
            space_401k = self.get_401k_normal_contribution_limit()
            space_401k += self.get_income() * self.employer_match_401k
            space += min(space_401k, self.get_401k_total_contribution_limit())
        return space

    def get_total_assets(self):
        """
        This is everything you own!
        """
        return (
            self.accounts.hsa.get_value()
            + self.accounts.taxable.get_value()
            + self.accounts.trad_ira.get_value()
            + self.accounts.trad_401k.get_value()
            + self.accounts.roth_ira.get_value()
            + self.accounts.roth_401k.get_value()
        )
    def do_roth_conversion(self):
        return self.is_retired() and not self.must_take_rmds()

    def get_roth_conversion_amount(self):
        """
        This is how much we will transfer from traditional 401k/IRA to your Roth
        IRA after retirement but before RMDs are required.
        """
        return self.roth_conversion_amount

    def get_estate_tax(self):
        return federal_taxes.calculate_estate_tax(self.get_total_assets())

    def get_taxes_for_heir(self):
        """
        This calculates the minimum tax your heir will be expected to pay as a
        result of RMDs. This assumes they have no income.
        """
        #
        # TODO: If the user specifies a dependent, use that to determine the
        # difference in age, rather than a hardcoded value. To simplify our
        # calculation, we can assume everything goes to the eldest child.
        #
        return federal_taxes.calculate_minimum_remaining_tax_for_heir(
            (
                self.accounts.trad_401k.get_value()
                + self.accounts.trad_ira.get_value()
            ),
            self.get_current_age() - 30
        )

    def get_death_tax(self):
        """
        This calculates how much we would owe if we died right now.

        Note: Do not sell stocks before death. They get a "step up in basis"
        meaning the basis changes. The heir will only be responsible for gains
        after inheritance.
        """
        return self.get_estate_tax() + self.get_taxes_for_heir()

    def get_total_taxes(self):
        return self.total_taxes

    def get_total_assets_after_death(self):
        return self.get_total_assets() - self.get_death_tax()

    def simulate_year(self):
        """
        This is a very long and complex function. It is hard to break it up into
        smaller chunks. There are basically two parts: contributions &
        withdrawals. We calculate the most we can contribute based on spending
        and taxes. Then, if we are retired, we withdrawal money from accounts in
        the most tax friendly order as possible.
        """
        tax_deductions = 0
        this_years_income = 0

        ########################################################################
        # Contributions
        ########################################################################

        hsa_contribution = 0
        taxable_contribution = 0
        roth_401k_contribution = 0
        roth_ira_contribution = 0
        trad_401k_contribution = 0
        trad_ira_contribution = 0
        employer_401k_contribution = 0

        #
        # These variables are used to binary search the maximum contribution.
        #
        minimum_contribution = 0
        total_contribution_limit = self.get_tax_advantaged_space()
        maximum_contribution = total_contribution_limit

        #
        # Alright, if we're still working, we can make some tax-advantaged
        # contributions. If there is a traditional contribution, it will lower
        # our taxes and, as a result, will allow us to contribute more! This is
        # why we must binary search the maximum contribution.
        #
        if not self.is_retired():
            this_years_income = self.get_income()

            #
            # We'll break out of this once the ideal amount is found.
            #
            while True:
                hsa_contribution = 0
                taxable_contribution = 0
                roth_401k_contribution = 0
                roth_ira_contribution = 0
                trad_401k_contribution = 0
                trad_ira_contribution = 0
                employer_401k_contribution = 0

                def whats_left_to_contribute():
                    return (
                        total_contribution_limit
                        - hsa_contribution
                        - roth_401k_contribution
                        - roth_ira_contribution
                        - trad_401k_contribution
                        - trad_ira_contribution
                    )

                #
                # First, we must get our employer HSA contribution. We are not
                # required to contribute anything for this.
                #
                hsa_contribution += min(
                    self.employer_contribution_hsa,
                    whats_left_to_contribute()
                )

                #
                # Next, we must get the employer 401k match. This is free money.
                #
                if self.prefer_roth():
                    roth_401k_contribution += min(
                        min(min(
                            self.get_income() * self.employer_match_401k,
                            self.get_401k_total_contribution_limit()
                        ), whats_left_to_contribute()),
                        self.get_income() * self.max_contribution_percentage_401k
                    )
                else:
                    trad_401k_contribution += min(
                        min(min(
                            self.get_income() * self.employer_match_401k,
                            self.get_401k_total_contribution_limit()
                        ), whats_left_to_contribute()),
                        self.get_income() * self.max_contribution_percentage_401k
                    )

                #
                # Add in the employer contribution. Normally, this is always
                # going to the pre-tax (traditional) bucket.
                #
                employer_401k_contribution = min(
                        min(min(
                            self.get_income() * self.employer_match_401k,
                            self.get_401k_total_contribution_limit()
                        ), whats_left_to_contribute()),
                        self.get_income() * self.max_contribution_percentage_401k
                    )
                trad_401k_contribution += employer_401k_contribution

                #
                # Next, contribute to your HSA since it is the ultimate
                # retirement account.
                #
                # https://www.madfientist.com/ultimate-retirement-account/
                #
                hsa_contribution += min(min(
                    this_years_income,
                    self.get_hsa_contribution_limit() - hsa_contribution
                ), whats_left_to_contribute())

                #
                # Calculate 401k contribution. Employer match does not count
                # towards the normal 401k limit.
                #
                if self.prefer_roth():
                    roth_401k_contribution += min(
                        min(min(
                            this_years_income,
                            self.get_401k_normal_contribution_limit() - employer_401k_contribution
                        ), whats_left_to_contribute()),
                        self.get_income() * (
                            self.max_contribution_percentage_401k
                            - self.employer_match_401k
                        )
                    )
                else:
                    trad_401k_contribution += min(
                        min(min(
                            this_years_income,
                            self.get_401k_normal_contribution_limit() - employer_401k_contribution
                        ), whats_left_to_contribute()),
                        self.get_income() * (
                            self.max_contribution_percentage_401k
                            - self.employer_match_401k
                        )
                    )

                #
                # Calculate IRA contribution. If there are no tax deductions for
                # the traditional IRA (because our income is too high) we might
                # as well contribute to Roth.
                #
                would_be_ira_contribution = min(
                    min(this_years_income, self.get_ira_contribution_limit()),
                    whats_left_to_contribute()
                )

                would_be_agi_if_trad = (
                    this_years_income
                    - hsa_contribution
                    - trad_401k_contribution
                    + employer_401k_contribution # Employer match doesn't lower AGI.
                    - would_be_ira_contribution
                )

                #
                # TODO: Maybe add a more granular approach, rather than an all
                # or nothing approach.
                #
                if self.prefer_roth() or not federal_taxes.fully_tax_deductible_ira(
                        would_be_agi_if_trad, self.is_married()):
                    roth_ira_contribution += would_be_ira_contribution
                else:
                    trad_ira_contribution += would_be_ira_contribution

                #
                # Calculate Mega-Backdoor Roth contribution, if applicable.
                #
                if self.do_mega_backdoor_roth():
                    after_tax_contribution = min(
                        min(
                            this_years_income,
                            (
                                self.get_401k_total_contribution_limit()
                                - trad_401k_contribution
                                - roth_401k_contribution
                            )
                        ),
                        whats_left_to_contribute()
                    )
                    roth_ira_contribution += after_tax_contribution

                tax_deductions = (
                    hsa_contribution
                    + trad_401k_contribution
                    - employer_401k_contribution
                    + trad_ira_contribution
                )

                #
                # We know about all of our tax deductions, we can accurately
                # calculate our taxes now. HSAs are not taxed by FICA.
                #
                taxable_income = max(this_years_income - tax_deductions, 0)
                fica_tax = federal_taxes.calculate_fica_tax(
                    this_years_income - hsa_contribution,
                    self.is_married()
                )
                federal_income_tax = federal_taxes.calculate_federal_income_tax(
                    taxable_income,
                    self.is_married(),
                    self.get_num_dependents()
                )
                federal_income_tax -= federal_taxes.calculate_savers_credit(
                    taxable_income,
                    (
                        #
                        # HSA is not to be included in this list.
                        #
                        roth_401k_contribution
                        + trad_401k_contribution
                        - employer_401k_contribution
                        + roth_ira_contribution
                        + trad_ira_contribution
                    ),
                    self.is_married()
                )
                state_tax = state_taxes.calculate_state_tax(
                    taxable_income,
                    self.is_married(),
                    self.get_current_state(),
                    self.get_num_dependents()
                )

                #
                # We can't have negative taxes. The saver's credit could
                # potentially be more than our total federal income tax.
                #
                federal_income_tax = max(federal_income_tax, 0)

                result = (
                    this_years_income
                    - self.get_spending()
                    - fica_tax
                    - federal_income_tax
                    - state_tax
                    - hsa_contribution
                    - roth_401k_contribution
                    - trad_401k_contribution
                    + employer_401k_contribution
                    + self.employer_contribution_hsa
                    - roth_ira_contribution
                    - trad_ira_contribution
                )

                #
                # Binary search our way to the ideal contribution. We want the
                # result to be zero, which will happen when there is no leftover
                # money after taxes.
                #
                if round(result, 5) > 0:
                    if total_contribution_limit == self.get_tax_advantaged_space():
                        break
                    minimum_contribution = total_contribution_limit
                    total_contribution_limit = (
                        minimum_contribution
                        + maximum_contribution
                    )/2
                elif round(result, 5) < 0:
                    if total_contribution_limit == 0:
                        break
                    maximum_contribution = total_contribution_limit
                    total_contribution_limit = (
                        minimum_contribution
                        + maximum_contribution
                    )/2
                else:
                    break

            #
            # XXX: We'll handle taxable contributions later, in the withdrawals
            # section. But now that I think about it, maybe we should move it up
            # here. It would make more sense.
            #
            self.accounts.hsa.contribute(hsa_contribution)
            self.accounts.roth_401k.contribute(roth_401k_contribution)
            self.accounts.trad_401k.contribute(trad_401k_contribution)
            self.accounts.roth_ira.contribute(roth_ira_contribution)
            self.accounts.trad_ira.contribute(trad_ira_contribution)

        ########################################################################
        # Required Minimum Distribution (RMD) Calculations
        ########################################################################

        trad_401k_rmd = 0
        trad_ira_rmd = 0
        if self.must_take_rmds():
            trad_401k_rmd = self.get_rmd(self.accounts.trad_401k.get_value())
            trad_ira_rmd = self.get_rmd(self.accounts.trad_ira.get_value())

        ########################################################################
        # Withdrawals
        ########################################################################

        bare_minimum_withdrawal = trad_401k_rmd + trad_ira_rmd
        if self.do_roth_conversion():
            bare_minimum_withdrawal += self.get_roth_conversion_amount()
        minimum_withdrawal = bare_minimum_withdrawal
        total_withdrawal = bare_minimum_withdrawal
        maximum_withdrawal = self.get_total_assets()
        penalty_fees = 0

        while True:
            hsa_withdrawal = 0
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
                    - hsa_withdrawal
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
            # TODO: Enforce the 5 year maturity rule.
            #
            if self.do_roth_conversion():
                trad_401k_conversion = min(
                    self.accounts.trad_401k.get_value() - trad_401k_withdrawal,
                    self.get_roth_conversion_amount()
                )
                trad_ira_conversion = min(
                    self.accounts.trad_ira.get_value() - trad_ira_withdrawal,
                    self.get_roth_conversion_amount() - trad_401k_conversion
                )

                conversion_amount = trad_401k_conversion + trad_ira_conversion
                trad_401k_withdrawal += trad_401k_conversion
                trad_ira_withdrawal += trad_ira_conversion

            #
            # If we can withdrawal money without penalty, we should at least
            # withdrawal the standard deduction, because this will not have
            # federal income taxes and it will reduce our RMDs later.
            #
            if self.can_make_401k_withdrawal_penalty_free():
                trad_401k_withdrawal += min(min(
                    self.accounts.trad_401k.get_value() - trad_401k_withdrawal,
                    max((
                        federal_taxes.get_standard_deduction(self.is_married())
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
            if self.can_make_ira_withdrawal_penalty_free():
                taxable_withdrawal += min(min(
                    self.accounts.taxable.get_value() - taxable_withdrawal,
                    whats_left_to_withdrawal()
                ), max(federal_taxes.zero_tax_ltcg_income(self.is_married()) - (
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
            if self.can_make_ira_withdrawal_penalty_free():
                trad_ira_withdrawal += min(min(
                    self.accounts.trad_ira.get_value() - trad_ira_withdrawal,
                    max((
                        federal_taxes.get_standard_deduction(self.is_married())
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
                self.accounts.taxable.get_value() - taxable_withdrawal,
                whats_left_to_withdrawal()
            ), max(federal_taxes.zero_tax_ltcg_income(self.is_married()) - (
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
                self.accounts.trad_401k.get_value() - trad_401k_withdrawal,
                max((
                    federal_taxes.get_standard_deduction(self.is_married())
                    - this_years_income
                    - trad_401k_withdrawal
                    - trad_ira_withdrawal
                ), 0)
            ), whats_left_to_withdrawal())

            #
            # If the trad 401k runs out of money, this will cover the rest.
            #
            trad_ira_withdrawal += min(min(
                self.accounts.trad_ira.get_value() - trad_ira_withdrawal,
                max((
                    federal_taxes.get_standard_deduction(self.is_married())
                    - this_years_income
                    - trad_401k_withdrawal
                    - trad_ira_withdrawal
                ), 0)
            ), whats_left_to_withdrawal())

            #
            # This will be penalty free.
            #
            roth_401k_withdrawal += min(
                self.accounts.roth_401k.get_contributions() - roth_401k_withdrawal,
                whats_left_to_withdrawal()
            )
            roth_ira_withdrawal += min(
                self.accounts.roth_ira.get_contributions() - roth_ira_withdrawal,
                whats_left_to_withdrawal()
            )

            #
            # Time to drain our taxable account. Everything else will cost us.
            # LTCG will be cheaper than income tax.
            #
            taxable_withdrawal += min(
                self.accounts.taxable.get_value() - taxable_withdrawal,
                whats_left_to_withdrawal()
            )

            #
            # We'll have to pay some level of income tax on this.
            #
            trad_401k_withdrawal += min(
                self.accounts.trad_401k.get_value() - trad_401k_withdrawal,
                whats_left_to_withdrawal()
            )
            trad_ira_withdrawal += min(
                self.accounts.trad_ira.get_value() - trad_ira_withdrawal,
                whats_left_to_withdrawal()
            )

            #
            # We're old, we need money, and we've run out of money in other
            # accounts. Non-qualified withdrawals will be treated as income.
            #
            if self.can_make_hsa_withdrawal_penalty_free():
                hsa_withdrawal += min(
                    self.accounts.hsa.get_value() - hsa_withdrawal,
                    whats_left_to_withdrawal()
                )

            #
            # Unless we're younger than 60, we'll have to pay income tax on the
            # gains. If we're this far, that means we have already extracted all
            # of our contributions, meaning this whole thing will be treated as
            # income.
            #
            roth_401k_with_interest_withdrawal += min(
                self.accounts.roth_401k.get_value() - roth_401k_withdrawal,
                whats_left_to_withdrawal()
            )
            roth_ira_with_interest_withdrawal += min(
                self.accounts.roth_ira.get_value() - roth_ira_withdrawal,
                whats_left_to_withdrawal()
            )

            #
            # I think that HSA early withdrawal penalties are the worse and, as
            # of 2021, you must be five years older than other retirement
            # accounts.
            #
            hsa_withdrawal += min(
                self.accounts.hsa.get_value() - hsa_withdrawal,
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
            if not self.can_make_ira_withdrawal_penalty_free():
                penalty_fees += roth_ira_withdrawal * 0.10
                penalty_fees += trad_ira_withdrawal * 0.10
            if not self.can_make_401k_withdrawal_penalty_free():
                penalty_fees += roth_401k_withdrawal * 0.10
                penalty_fees += trad_401k_withdrawal * 0.10

            #
            # If you are under age 65, you pay a 20% penalty on nonmedical
            # withdrawals, and you pay the tax in addition to the penalty.
            #
            if not self.can_make_hsa_withdrawal_penalty_free():
                penalty_fees += hsa_withdrawal * 0.20

            #
            # If you’re over 59½ and your account is at least five years old,
            # you can withdraw contributions and earnings with no tax or
            # penalty. We don't support half ages.
            #
            if self.roth_gains_are_taxable():
                roth_gains += self.accounts.roth_401k.withdrawal(
                    roth_401k_with_interest_withdrawal,
                    dry_run=True
                ).get_gains()
                roth_gains += self.accounts.roth_ira.withdrawal(
                    roth_ira_with_interest_withdrawal,
                    dry_run=True
                ).get_gains()

            taxable_income = max(round(
                this_years_income
                + trad_401k_withdrawal
                + trad_ira_withdrawal
                + roth_gains
                + (0 if self.can_make_hsa_withdrawal_penalty_free() else hsa_withdrawal)
                - tax_deductions,
                2
            ), 0)

            #
            # Now that we know our taxable income, we can calculate LTCG tax.
            #
            if taxable_withdrawal:
                withdrawal = self.accounts.taxable.withdrawal(
                    taxable_withdrawal,
                    dry_run=True
                )
                ltcg_taxes = federal_taxes.calculate_federal_income_tax(
                    taxable_income, self.is_married(),
                    ltcg=withdrawal.get_gains(),
                    just_ltcg=True
                )

            #
            # When calculating the FICA tax, we must not include retirement
            # distributions. These have already been taxed by FICA.
            #
            fica_tax = federal_taxes.calculate_fica_tax(
                this_years_income - hsa_contribution,
                self.is_married()
            )

            #
            # Calculate the federal taxes. This includes the federal income tax
            # and FICA (social security and medicare) tax.
            #
            federal_income_tax = federal_taxes.calculate_federal_income_tax(
                taxable_income,
                self.is_married(),
                self.get_num_dependents()
            )

            #
            # Calculate saver's credit. This provides tax credits if you are low
            # income and made retirement contributions.
            #
            if not self.is_retired():
                savers_credit = federal_taxes.calculate_savers_credit(
                    taxable_income,
                    (
                        roth_401k_contribution
                        + roth_ira_contribution
                        + trad_401k_contribution
                        + trad_ira_contribution
                    ),
                    self.is_married()
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
                self.is_married(),
                self.get_current_state(),
                self.get_num_dependents()
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
                + employer_401k_contribution
                + self.employer_contribution_hsa
                - this_years_taxes
                - self.get_spending()
                - hsa_contribution
                - taxable_contribution
                - roth_401k_contribution
                - roth_ira_contribution
                - trad_401k_contribution
                - trad_ira_contribution
                - conversion_amount
                - penalty_fees
                + hsa_withdrawal
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
                    self.accounts.taxable.contribute(taxable_contribution)
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
                if round(total_withdrawal, 2) == round(self.get_total_assets(), 2):
                    self.needed_to_continue = abs(result)
                    break
                minimum_withdrawal = total_withdrawal
                total_withdrawal = (
                    minimum_withdrawal
                    + maximum_withdrawal
                )/2
            else:
                break

        withdrawals = [
            self.accounts.hsa.withdrawal(hsa_withdrawal),
            self.accounts.taxable.withdrawal(taxable_withdrawal),
            self.accounts.trad_401k.withdrawal(trad_401k_withdrawal),
            self.accounts.trad_ira.withdrawal(trad_ira_withdrawal),
            self.accounts.roth_401k.withdrawal(roth_401k_withdrawal),
            self.accounts.roth_401k.withdrawal(roth_401k_with_interest_withdrawal),
            self.accounts.roth_ira.withdrawal(roth_ira_withdrawal),
            self.accounts.roth_ira.withdrawal(roth_ira_with_interest_withdrawal)
        ]
        for withdrawal in withdrawals:
            assert withdrawal.get_insufficient() == 0, withdrawal

        #
        # Now is the time to do the Roth conversion.
        #
        roth_ira_contribution += conversion_amount
        self.accounts.roth_ira.contribute(conversion_amount, rollover=True)

        #
        # Now that we've finalized our withdrawals, we know our taxes.
        #
        self.total_taxes += this_years_taxes

        ########################################################################
        # Data Collection
        ########################################################################

        this_years_federal_taxes = federal_income_tax + fica_tax

        #
        # We have finished the year. Add an entry to the table. This will get
        # printed when the simulation is over.
        #
        self.table.add_row(
            f"{self.get_current_age()}",
            ":heart_eyes:" if self.is_married() else "",
            ":tada:" if self.is_retired() else "",
            f"{self.accounts.hsa.get_value():,.2f}" if self.accounts.hsa.get_value() else "",
            f"{self.accounts.hsa.get_yearly_diff()}",
            f"{self.accounts.roth_401k.get_value():,.2f}" if self.accounts.roth_401k.get_value() else "",
            f"{self.accounts.roth_401k.get_yearly_diff()}",
            f"{self.accounts.roth_ira.get_value():,.2f}" if self.accounts.roth_ira.get_value() else "",
            f"{self.accounts.roth_ira.get_yearly_diff()}",
            f"{self.accounts.taxable.get_value():,.2f}" if self.accounts.taxable.get_value() else "",
            f"{self.accounts.taxable.get_yearly_diff()}",
            f"{self.accounts.trad_401k.get_value():,.2f}" if self.accounts.trad_401k.get_value() else "",
            f"{self.accounts.trad_401k.get_yearly_diff()}",
            f"[yellow]{trad_401k_rmd:,.2f}[/yellow]" if trad_401k_rmd else "",
            f"{self.accounts.trad_ira.get_value():,.2f}" if self.accounts.trad_ira.get_value() else "",
            f"{self.accounts.trad_ira.get_yearly_diff()}",
            f"[yellow]{trad_ira_rmd:,.2f}[/yellow]" if trad_ira_rmd else "",
            f"[cyan]{self.get_income():,.2f}[/cyan]" if self.get_income() else "",
            f"[red]{self.get_spending():,.2f}[/red]" if self.get_spending() else "",
            f"{self.get_num_dependents():d}" if self.get_num_dependents() else "",
            f"{self.get_current_state()}",
            f"[red]{state_tax:,.2f}[/red]" if state_tax else "",
            f"[red]{penalty_fees:,.2f}[/red]" if penalty_fees else "",
            f"[red]{this_years_federal_taxes:,.2f}[/red]" if this_years_federal_taxes else "",
            f"[purple]{self.get_total_taxes():,.2f}[/purple]" if self.get_total_taxes() else "",
        )

    def increment_year(self):
        """
        Happy new year! Apply interest to all of our accounts.
        """
        self.year += 1

        #
        # The increment function adds this year's returns to the account.
        #
        self.accounts.hsa.increment()
        self.accounts.taxable.increment()
        self.accounts.roth_401k.increment()
        self.accounts.roth_ira.increment()
        self.accounts.trad_401k.increment()
        self.accounts.trad_ira.increment()

    def simulate(self):
        """
        This will simulate until we can no longer simulate.
        """
        while not self.stop_simulation():
            self.simulate_year()
            self.increment_year()

        #
        # Once we are finished, we are dead or ran out of money. In either case,
        # we should add death tax to our total taxes.
        #
        self.total_taxes += self.get_death_tax()

    def get_params_table(self):
        return self.params_table

    def get_math_table(self):
        return self.table

    def get_summary_table(self):
        """
        This function creates a summary of your financial life.
        """
        try:
            tax_to_asset_ratio = self.get_total_taxes()/self.get_total_assets()
        except ZeroDivisionError:
            tax_to_asset_ratio = None

        summary_table = Table(show_header=True, header_style="bold magenta")
        summary_table.add_column("Field")
        summary_table.add_column("Value at Death", justify="right")
        summary_table.add_row("HSA", f"{self.accounts.hsa.get_value():,.2f}")
        summary_table.add_row("Taxable", f"{self.accounts.taxable.get_value():,.2f}")
        summary_table.add_row("Trad 401k", f"{self.accounts.trad_401k.get_value():,.2f}")
        summary_table.add_row("Trad IRA", f"{self.accounts.trad_ira.get_value():,.2f}")
        summary_table.add_row("Roth 401k", f"{self.accounts.roth_401k.get_value():,.2f}")
        summary_table.add_row("Roth IRA", f"{self.accounts.roth_ira.get_value():,.2f}")
        summary_table.add_row("Min Tax for Heir", f"{self.get_taxes_for_heir():,.2f}")
        summary_table.add_row("Estate Taxes", f"{self.get_estate_tax():,.2f}")
        summary_table.add_row("Total Taxes", f"{self.get_total_taxes():,.2f}")
        summary_table.add_row("Total Assets", f"{self.get_total_assets():,.2f}")
        summary_table.add_row("Total Assets After Taxes", f"{max(self.get_total_assets_after_death(), 0):,.2f}")
        summary_table.add_row("Tax/Asset Ratio", f"{tax_to_asset_ratio:,.2f}" if tax_to_asset_ratio else "")
        return summary_table


def main():
    """
    This function parses user input and runs the simulation.
    """
    parser = argparse.ArgumentParser(
        description="Wealth Simulator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--current-age",
        help="How old are you currently?",
        required=False,
        type=int,
        default=38
    )
    parser.add_argument(
        "--income",
        help="What is your current income?",
        required=False,
        type=float,
        default=63179
    )
    parser.add_argument(
        "--max-income",
        help="What will your income max out at?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--starting-balance-hsa",
        help="Starting balance for HSA account?",
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
        "--contribution-limit-hsa",
        help="What is the individual HSA contribution limit?",
        required=False,
        type=float,
        default=3600
    )
    parser.add_argument(
        "--employer-contribution-hsa",
        help="How much does your employer contribution to your HSA?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--contribution-catch-up-amount-hsa",
        help="How much extra can you contribute at this age?",
        required=False,
        type=float,
        default=1000
    )
    parser.add_argument(
        "--contribution-catch-up-age-hsa",
        help="At what age can you do extra catch up contributions?",
        required=False,
        type=int,
        default=55
    )
    parser.add_argument(
        "--contribution-limit-401k",
        help="What is the normal 401k contribution limit?",
        required=False,
        type=float,
        default=19500
    )
    parser.add_argument(
        "--contribution-limit-401k-total",
        help="What is the total 401k contribution limit?",
        required=False,
        type=float,
        default=58000
    )
    parser.add_argument(
        "--contribution-catch-up-amount-401k",
        help="How much extra can you contribute at this age?",
        required=False,
        type=float,
        default=6500
    )
    parser.add_argument(
        "--contribution-catch-up-age-401k",
        help="At what age can you do 401k catch up contributions?",
        required=False,
        type=float,
        default=50
    )
    parser.add_argument(
        "--employer-match-401k",
        help="How much does your employer match your contribution? (0.0 - 1.0)",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--max-contribution-percentage-401k",
        help="Does your employer restrict how much of your paycheck you can contribute? (0.0 - 1.0)",
        required=False,
        type=float,
        default=1.0
    )
    parser.add_argument(
        "--contribution-limit-ira",
        help="What is the IRA contribution limit?",
        required=False,
        type=float,
        default=6000
    )
    parser.add_argument(
        "--contribution-catch-up-amount-ira",
        help="How much extra can you contribute at this age?",
        required=False,
        type=float,
        default=1000
    )
    parser.add_argument(
        "--contribution-catch-up-age-ira",
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
        help="Years to wait before doing traditional (pre-tax) contributions",
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

    try:
        #
        # TODO: Use concurrent.futures to make this faster.
        #
        with Live(transient=True, refresh_per_second=144) as live:
            while True:
                simulation = Simulation(
                    args.starting_balance_hsa,
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
                    args.contribution_limit_hsa,
                    args.contribution_catch_up_amount_hsa,
                    args.contribution_catch_up_age_hsa,
                    args.contribution_limit_401k,
                    args.contribution_limit_401k_total,
                    args.contribution_catch_up_amount_401k,
                    args.contribution_catch_up_age_401k,
                    args.contribution_limit_ira,
                    args.contribution_catch_up_amount_ira,
                    args.contribution_catch_up_age_ira,
                    args.do_mega_backdoor_roth,
                    args.work_state,
                    args.retirement_state,
                    args.add_dependent,
                    args.public_safety_employee,
                    args.employer_match_401k,
                    args.max_contribution_percentage_401k,
                    args.employer_contribution_hsa
                )

                live.update("Simulating with Roth conversion: "
                            f"{roth_conversion_amount:,.2f}")
                simulation.simulate()

                if round(simulation.get_total_assets_after_death(), 2) >= round(most_assets, 2):
                    best_roth_conversion_amount = roth_conversion_amount
                    most_assets = simulation.get_total_assets_after_death()

                traditional_money = (
                    simulation.accounts.trad_401k.get_value()
                    + simulation.accounts.trad_ira.get_value()
                )
                if round(traditional_money, 2) == 0:
                    break
                roth_conversion_amount += args.roth_conversion_unit

        #
        # Now that we know all of the variables, run the simulation.
        #
        simulation = Simulation(
            args.starting_balance_hsa,
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
            args.contribution_limit_hsa,
            args.contribution_catch_up_amount_hsa,
            args.contribution_catch_up_age_hsa,
            args.contribution_limit_401k,
            args.contribution_limit_401k_total,
            args.contribution_catch_up_amount_401k,
            args.contribution_catch_up_age_401k,
            args.contribution_limit_ira,
            args.contribution_catch_up_amount_ira,
            args.contribution_catch_up_age_ira,
            args.do_mega_backdoor_roth,
            args.work_state,
            args.retirement_state,
            args.add_dependent,
            args.public_safety_employee,
            args.employer_match_401k,
            args.max_contribution_percentage_401k,
            args.employer_contribution_hsa
        )
        simulation.simulate()
    except KeyboardInterrupt:
        return

    #
    # Print stuff to the console if the user wants it.
    #
    console = Console()
    if args.show_params:
        console.print(simulation.get_params_table())
    if args.show_math:
        console.print(simulation.get_math_table())
    if args.show_summary:
        console.print(simulation.get_summary_table())

    #
    # If the user didn't specify to show anything, print the math table.
    #
    if not any([args.show_params, args.show_math, args.show_summary]):
        console.print(simulation.get_math_table())

    if simulation.get_needed_to_continue():
        console.print(":fire::fire::fire: Please enter "
                      f"[underline]{simulation.get_needed_to_continue():,.2f}[/underline]"
                      " to continue playing. :fire::fire::fire:")

if __name__ == "__main__":
    main()
