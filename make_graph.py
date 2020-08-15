#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt

from rmds import calculate_rmds

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
    parser.add_argument(
        "--verbose",
        help="Do things and talk more",
        action="store_true"
    )

    args = parser.parse_args()

    def my_calculate_rmds(interest_rate, years_to_wait):
        return calculate_rmds(
            args.principal_traditional,
            args.principal_roth,

            #
            # Our first variable.
            #
            interest_rate,

            args.yearly_contribution_traditional,
            args.yearly_contribution_roth,

            #
            # Our second variable.
            #
            years_to_wait,

            args.current_age,
            args.age_of_retirement,
            args.age_to_start_rmds,
            args.age_at_death,
            args.roth_rollover_amount,
            args.income,
            args.yearly_income_raise,
            args.max_income,
            args.age_of_marriage,
            args.verbose
        )

    def scale(l):
        """So because of compound interest, the higher the interest rate the
        less you will pay in taxes. This can be a pretty wide range. Looks bad.
        They just look like straight lines. I'm not really sure how to do this,
        but I looked up "how to normalize data" and featured scaling looked
        right. Link: https://en.wikipedia.org/wiki/Feature_scaling
        """
        def _scale(v):
            return (v - min(l))/(max(l) - min(l))
        return list(map(_scale, l))

    #
    # Generate our outputs.
    #
    for interest_rate in [1.01, 1.02, 1.03, 1.04, 1.05, 1.06]:
        inputs = range(args.age_of_retirement - args.current_age)
        outputs = list(map(lambda y: my_calculate_rmds(interest_rate, y), inputs))
        plt.plot(inputs, scale(outputs), label=str(interest_rate))

    plt.xlabel("Years to Wait")
    plt.ylabel("Taxes to Assets Ratio (scaled)")
    plt.title("When to Start Pre-Tax Contributions?")

    plt.legend()
    plt.show()
