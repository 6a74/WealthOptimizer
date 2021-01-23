#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import progressbar

import sim

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make a tax graph",
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
        "--principal-taxable",
        help="Starting balance for taxable (after-tax) accounts?",
        required=False,
        type=float,
        default=0
    )
    parser.add_argument(
        "--principal-traditional",
        help="Starting balance for traditional (pre-tax) accounts?",
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
        "--yearly-401k-contribution",
        help="How much are you contributing to your 401k per year?",
        required=False,
        type=float,
        default=19500
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
        "--yearly-ira-contribution",
        help="How much are you contributing to your IRA per year?",
        required=False,
        type=float,
        default=6000
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
        help="How much extra can you contribute at the age of 50?",
        required=False,
        type=float,
        default=1000
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
        "--verbose",
        help="Do things and talk more",
        action="store_true"
    )

    args = parser.parse_args()

    def my_calculation(return_rate, start_with_roth):
        #
        # Calculate the most efficient Roth conversion amount.
        #
        most_assets = 0
        roth_conversion_amount = 0
        best_roth_conversion_amount = 0

        if args.age_of_death > args.age_of_retirement:
            for x in range(1000):
                assets = sim.calculate_assets(
                    args.principal_taxable,
                    args.principal_traditional,
                    args.principal_roth,
                    return_rate,
                    args.yearly_401k_contribution,
                    start_with_roth,
                    args.current_age,
                    args.age_of_retirement,
                    args.age_to_start_rmds,
                    args.age_of_death,
                    roth_conversion_amount,
                    args.income,
                    args.yearly_income_raise,
                    args.max_income,
                    args.age_of_marriage,
                    args.spending,
                    args.yearly_401k_normal_contribution_limit,
                    args.yearly_401k_total_contribution_limit,
                    args.yearly_ira_contribution,
                    args.yearly_ira_contribution_limit,
                    args.ira_contribution_catch_up,
                    args.do_mega_backdoor_roth,
                    debug=False
                )
                if assets > most_assets:
                    best_roth_conversion_amount = roth_conversion_amount
                    most_assets = assets
                if assets < most_assets:
                    break
                roth_conversion_amount += 1000

        return sim.calculate_assets(
            args.principal_taxable,
            args.principal_traditional,
            args.principal_roth,
            return_rate,
            args.yearly_401k_contribution,
            start_with_roth,
            args.current_age,
            args.age_of_retirement,
            args.age_to_start_rmds,
            args.age_of_death,
            best_roth_conversion_amount,
            args.income,
            args.yearly_income_raise,
            args.max_income, args.age_of_marriage,
            args.spending,
            args.yearly_401k_normal_contribution_limit,
            args.yearly_401k_total_contribution_limit,
            args.yearly_ira_contribution,
            args.yearly_ira_contribution_limit,
            args.ira_contribution_catch_up,
            args.do_mega_backdoor_roth,
            args.verbose
        )

    def scale(l):
        """Depending on the variables, these values can be part of a pretty wide
        range, which looks bad. In my experience, unscaled graphs just look like
        straight lines. I'm not really an expert in normalizing data, so I just
        looked up "how to normalize data" and featured scaling looked right.
        Link: https://en.wikipedia.org/wiki/Feature_scaling
        """
        def _scale(v):
            return (v - min(l))/(max(l) - min(l))
        return list(map(_scale, l))

    #
    # Generate our outputs.
    #
    working_years = args.age_of_retirement - args.current_age
    return_rates = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07]
    colors = ['tab:blue', 'tab:red', 'tab:orange', 'tab:purple', 'tab:brown', 'tab:olive', 'tab:cyan']

    assert working_years >= 0

    best_indices = []
    current_calculation = 0
    num_calculations = working_years * len(return_rates)
    with progressbar.ProgressBar(max_value=num_calculations) as bar:
        for return_rate, color in zip(return_rates, colors):
            inputs = range(working_years)
            outputs = []
            for y in inputs:
                outputs.append(my_calculation(return_rate, y))
                current_calculation += 1
                bar.update(current_calculation)

            plt.plot(
                inputs,
                scale(outputs),
                label=f"Rate of Return: {return_rate:.2f}",
                linestyle='-',
                color=color
            )

            best_index = 0
            most_assets = 0
            for index, assets in enumerate(outputs):
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
        ["Current Age", f"{args.current_age}"],
        ["Age of Marriage", f"{args.age_of_marriage}"],
        ["Age of Retirement", f"{args.age_of_retirement}"],
        ["Age to Start RMDs", f"{args.age_to_start_rmds}"],
        ["Age of Death", f"{args.age_of_death}"],
        ["Current Income", f"${args.income:,.2f}"],
        ["Max Income", f"${args.max_income:,.2f}"],
        ["Yearly Spending", f"${args.spending:,.2f}"],
        ["Yearly Income Raise", f"{args.yearly_income_raise:.2f}"],
        ["Starting Taxable Balance", f"${args.principal_taxable:,.2f}"],
        ["Starting Traditional Balance", f"${args.principal_traditional:,.2f}"],
        ["Starting Roth Balance", f"${args.principal_roth:,.2f}"],
        ["Starting 401k Contribution", f"${args.yearly_401k_contribution:,.2f}"],
        ["401k Normal Contribution Limit", f"${args.yearly_401k_normal_contribution_limit:,.2f}"],
        ["401k Total Contribution Limit", f"${args.yearly_401k_total_contribution_limit:,.2f}"],
        ["Starting IRA Contribution", f"${args.yearly_ira_contribution:,.2f}"],
        ["IRA Contribution Limit", f"${args.yearly_ira_contribution_limit:,.2f}"],
        ["Mega-Backdoor Roth", args.do_mega_backdoor_roth],
    ]

    the_table = plt.table(cellText=cells, bbox=[1.05, 0.25, 0.5, 0.75])
    the_table.auto_set_font_size(False)
    plt.subplots_adjust(right=0.65)

    #plt.legend()
    plt.legend(bbox_to_anchor=(1.045, 0), loc="lower left")
    plt.show()
