#!/usr/bin/env python3

import argparse
import concurrent.futures
import itertools
import matplotlib.pyplot as plt

from rich.progress import Progress

import state_taxes

from sim import Simulation


def my_calculation(arguments):
    """
    This function returns the assets after death for the given arguments.
    """
    args, rate_of_return, years_to_wait = arguments

    #
    # Calculate the most efficient Roth conversion amount.
    #
    most_assets = 0
    roth_conversion_amount = 0
    best_roth_conversion_amount = 0

    while True:
        simulation = Simulation(
            args.starting_balance_hsa,
            args.starting_balance_taxable,
            args.starting_balance_trad_401k,
            args.starting_balance_trad_ira,
            args.starting_balance_roth_401k,
            args.starting_balance_roth_ira,
            rate_of_return,
            years_to_wait,
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

    simulation = Simulation(
        args.starting_balance_hsa,
        args.starting_balance_taxable,
        args.starting_balance_trad_401k,
        args.starting_balance_trad_ira,
        args.starting_balance_roth_401k,
        args.starting_balance_roth_ira,
        rate_of_return,
        years_to_wait,
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
    return simulation.get_total_assets_after_death()


def main():
    parser = argparse.ArgumentParser(
        description="Make a tax graph",
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

    args = parser.parse_args()

    def scale(values):
        """
        Depending on the variables, these values can be part of a pretty wide
        range, which looks bad. In my experience, unscaled graphs just look like
        straight lines. I'm not really an expert in normalizing data, so I just
        looked up "how to normalize data" and featured scaling looked right.

        Link: https://en.wikipedia.org/wiki/Feature_scaling
        """
        def _scale(val):
            return (val - min(values))/(max(values) - min(values))
        return list(map(_scale, values))

    #
    # Generate our outputs.
    #
    working_years = args.age_of_retirement - args.current_age
    return_rates = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07]
    colors = [
        'tab:blue', 'tab:red', 'tab:orange', 'tab:purple',
        'tab:brown', 'tab:olive', 'tab:cyan'
    ]

    assert working_years >= 0

    best_indices = []
    num_calculations = working_years * len(return_rates)
    with Progress() as progress:
        task = progress.add_task("Calculating:", total=num_calculations)
        for rate_of_return, color in zip(return_rates, colors):
            inputs = list(range(working_years))
            vals = []
            with concurrent.futures.ProcessPoolExecutor() as executor:
                for i, j in zip(inputs, executor.map(
                        my_calculation, itertools.product([args],
                        [rate_of_return], inputs))
                ):
                    progress.update(task, advance=1)
                    vals.append((i, j))
                vals = sorted(vals, key=lambda l: l[0])

            plt.plot(
                [v[0] for v in vals],
                scale([v[1] for v in vals]),
                label=f"Rate of Return: {rate_of_return:.2f}",
                linestyle='-',
                color=color
            )

            best_index = 0
            most_assets = 0
            for index, assets in enumerate([v[1] for v in vals]):
                if assets > most_assets:
                    best_index = index
                most_assets = max(most_assets, assets)

            while True:
                if best_index in best_indices:
                    best_index += 0.1
                if best_index not in best_indices:
                    break

            best_indices.append(best_index)
            plt.axvline(x=best_index, color=color, linestyle=':')

    plt.xlabel("Years to Wait Before Deferring Taxes")
    plt.ylabel("Estate At Death After Taxes")
    plt.title("When to Start Deferring Taxes?")

    cells = [
        ["Starting Age", f"{args.current_age}"],
        ["Age of Marriage", f"{args.age_of_marriage}"],
        ["Age of Retirement", f"{args.age_of_retirement}"],
        ["Age to Start RMDs", f"{args.age_to_start_rmds}"],
        ["Age of Death", f"{args.age_of_death}"],
        ["Current Income", f"${args.income:,.2f}"],
        ["Max Income", f"${args.max_income:,.2f}"],
        ["Yearly Spending", f"${args.spending:,.2f}"],
        ["Yearly Income Raise", f"{args.yearly_income_raise:.2f}"],
        ["HSA Starting Balance", f"${args.starting_balance_hsa:,.2f}"],
        ["Taxable Starting Balance", f"${args.starting_balance_taxable:,.2f}"],
        ["Trad 401k Starting Balance", f"${args.starting_balance_trad_401k:,.2f}"],
        ["Trad IRA Starting Balance", f"${args.starting_balance_trad_ira:,.2f}"],
        ["Roth 401k Starting Balance", f"${args.starting_balance_roth_401k:,.2f}"],
        ["Roth IRA Starting Balance", f"${args.starting_balance_roth_ira:,.2f}"],
        ["HSA Contribution Limit", f"${args.contribution_limit_hsa:,.2f}"],
        ["401k Normal Contribution Limit", f"${args.contribution_limit_401k:,.2f}"],
        ["401k Total Contribution Limit", f"${args.contribution_limit_401k_total:,.2f}"],
        ["IRA Contribution Limit", f"${args.contribution_limit_ira:,.2f}"],
        ["Mega-Backdoor Roth", args.do_mega_backdoor_roth],
        ["Work State", f"{args.work_state}"],
        ["Retirement State", f"{args.retirement_state}"],
        ["HSA Employer Contribution", f"{args.employer_contribution_hsa}"],
    ]

    the_table = plt.table(cellText=cells, bbox=[1.05, 0.25, 0.5, 0.75])
    the_table.auto_set_font_size(False)
    the_table.auto_set_column_width((0, 1))
    plt.subplots_adjust(right=0.65)

    plt.legend(bbox_to_anchor=(1.041, -0.01), loc="lower left")
    plt.show()

if __name__ == "__main__":
    main()
