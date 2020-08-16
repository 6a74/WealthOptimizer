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
        default=116
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
    parser.add_argument(
        "--verbose",
        help="Do things and talk more",
        action="store_true"
    )

    args = parser.parse_args()

    def my_calculation(interest_rate, years_to_wait):
        #
        # Calculate the most efficient Roth rollover amount.
        #
        min_tax_rate = 1.0
        roth_rollover_amount = 0

        if args.age_of_death > args.age_of_retirement:
            for x in range(1000):
                tax_rate = sim.calculate_tax_to_asset_ratio(
                    args.principal_traditional,
                    args.principal_roth,
                    interest_rate,
                    args.yearly_contribution_traditional,
                    args.yearly_contribution_roth,
                    years_to_wait,
                    args.current_age,
                    args.age_of_retirement,
                    args.age_to_start_rmds,
                    args.age_of_death,
                    roth_rollover_amount,
                    args.income,
                    args.yearly_income_raise,
                    args.max_income,
                    args.age_of_marriage,
                    debug=False
                )
                min_tax_rate = min(min_tax_rate, tax_rate)
                if tax_rate > min_tax_rate:
                    break
                roth_rollover_amount += 1000

        return sim.calculate_tax_to_asset_ratio(
            args.principal_traditional,
            args.principal_roth,
            interest_rate,
            args.yearly_contribution_traditional,
            args.yearly_contribution_roth,
            years_to_wait,
            args.current_age,
            args.age_of_retirement,
            args.age_to_start_rmds,
            args.age_of_death,
            roth_rollover_amount,
            args.income,
            args.yearly_income_raise,
            args.max_income,
            args.age_of_marriage,
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
    interest_rates = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06]

    assert working_years >= 0

    current_calculation = 0
    num_calculations = working_years * len(interest_rates)
    with progressbar.ProgressBar(max_value=num_calculations) as bar:
        for interest_rate in interest_rates:
            inputs = range(working_years)
            outputs = []
            for y in inputs:
                outputs.append(my_calculation(interest_rate, y))
                current_calculation += 1
                bar.update(current_calculation)
            plt.plot(inputs, scale(outputs), label=f"{interest_rate=:.2f}")

    plt.xlabel("Years to Wait")
    plt.ylabel("Taxes to Assets Ratio (scaled)")
    plt.title("When to Start Deferring Taxes?")

    cells = [
        ["Current Age", f"{args.current_age}"],
        ["Age of Marriage", f"{args.age_of_marriage}"],
        ["Age of Retirement", f"{args.age_of_retirement}"],
        ["Age to Start RMDs", f"{args.age_to_start_rmds}"],
        ["Age of Death", f"{args.age_of_death}"],
        ["Current Income", f"${args.income:,.2f}"],
        ["Max Income", f"${args.max_income:,.2f}"],
        ["Yearly Income Raise", f"{args.yearly_income_raise:.2f}"],
        ["Starting Trad Balance", f"${args.principal_traditional:,.2f}"],
        ["Starting Roth Balance", f"${args.principal_roth:,.2f}"],
        ["Yearly Trad Contrib", f"${args.yearly_contribution_traditional:,.2f}"],
        ["Yearly Roth Contrib", f"${args.yearly_contribution_roth:,.2f}"],
    ]

    plt.table(cellText=cells, bbox=[1.05,0.5,0.5,0.5])
    plt.subplots_adjust(right=0.65)

    plt.legend()
    plt.show()
