# When to Defer Taxes?

## Introduction

Many people in the [Bogleheads](https://www.bogleheads.org) community, a
fantastic resource for investing advice, believe that it is almost always better
to defer taxes (_i.e._ contribute to
[Traditional](https://www.bogleheads.org/wiki/Traditional_IRA) accounts rather
than [Roth](https://www.bogleheads.org/wiki/Roth_IRA) accounts). I would like to
make the case against the notion that deferring taxes is best for people that
can "max out" their retirement accounts, like many individuals that read
Bogleheads can do.

### Who Said Traditional is Better?

From the Bogleheads's [general
guidelines](https://www.bogleheads.org/wiki/Traditional_versus_Roth#General_guidelines)
on Traditional vs. Roth:

> Using 100% traditional because, for most people, traditional will be better

While this is probably correct, the typical Bogleheads reader is probably a
better saver.

### Who is the Typical Person?

* In 2018, the real median [household income in the
U.S.](https://en.wikipedia.org/wiki/Household_income_in_the_United_States) was
$63,179.
* In 2018, the [median
age](https://en.wikipedia.org/wiki/Demographics_of_the_United_States#Median_age_of_the_population)
is 38.2 years old.
* Between 2015 and 2020, the [expected life
expentancy](https://en.wikipedia.org/wiki/Demographics_of_the_United_States#Vital_statistics_2)
is 78.8 years.

## Argument

My core argument is based around [minimum required
distributions](https://www.bogleheads.org/wiki/Required_Minimum_Distribution)
(RMD). As the name suggests, these are IRS-mandated withdrawals from select
retirement accounts. If an investor puts too much money in tax-deferred
accounts, they might be forced to withdrawal large sums of money, which could be
heavily taxed. The alternative is to redirect those contributions to Roth
accounts, in which you pay taxes up-front and then (hopefully) never again.

## Figures

The following figures are generated with the `graph.py` utility. The values are
calculated with the `sim.calculate_tax_to_asset_ratio` method. Variables are:

* Real Interest Rate (1% - 6%, should satisfy everyone)
* Years to Wait (the number of years to wait before deferring taxes)

Note: In most figures, after a certain number of years, the tax rate grows at a
constant rate. This is due to there being so little in Traditional
(tax-deferred) accounts. RMDs are relativly small (less than your standard
deduction) and taxed generally taxed near (or at) 0%. After this point, it
becomes clearily detremental to not defer taxes.

The figure below shows a 20 year old starting from nothing. Unless the real
return over the next 80 years is 1% or less, Roth contributions appear to be the
logical choice for at least the next 10 years.

![Figure 1](https://github.com/6a74/finance/blob/master/figures/Figure_20.png?raw=true)

The figure below shows a 25 year old starting from nothing. This is very similar
to the figure above. Things are shifted by approximately five years; who would
have guessed?

![Figure 2](https://github.com/6a74/finance/blob/master/figures/Figure_25.png?raw=true)

The figure below shows a 25 year old with \$100k in Traditional and \$50k in Roth:

![Figure 2](https://github.com/6a74/finance/blob/master/figures/Figure_25_with_assets.png?raw=true)

The figure below shows a 40 year old starting from nothing:

![Figure 3](https://github.com/6a74/finance/blob/master/figures/Figure_40.png?raw=true)

This figure shows what values looks like without scaling:

![Figure 4](https://github.com/6a74/finance/blob/master/figures/Figure_20_noscale.png?raw=true)

The figure below shows a 20 year old that retires 10 years earlier (at 50):

![Figure 5](https://github.com/6a74/finance/blob/master/figures/Figure_20_retire_at_50.png?raw=true)

The figure below shows a 20 year old that retires 20 years earlier (at 40). Even
in this rather extreme situation, it might be better (if _real_ interest rates
are greater than 4%) to defer deferring taxes a few years.

![Figure 6](https://github.com/6a74/finance/blob/master/figures/Figure_20_retire_at_40.png?raw=true)

### Key Takeaways

* It _does_ makes sense to defer taxes later in one's career, just not always
  immediately.
* In very low interest rate (1%) scenarios, it is almost always better to defer
  taxes immediately.
* If you plan to retire very early (40), it appears to be better to defer
  taxes immediately.
* If long-term interest rates are high (6%+), it appears to be better to
  make Roth contributes.

## Utilities

### `sim.py`

This module contains the core function: `calculate_tax_to_asset_ratio`. Given
all of the initial variables, this function will "simulate" your portfolio and
return a "tax to assset" ratio. This is something I defined. I am unsure if this
is used elsewhere.

#### Tax to Asset Ratio

The tax to asset ratio (TAR) is the total amount paid in taxes (income, capital
gains) divided by total assets across all accounts (taxable, Roth, Traditional).
We use this to compare simulations with different interest rates. You cannot
compare simulations solely on assets or taxes. In higher interest rate
simulations, more interest in accrued and as a result more taxes are required.
In this situation, that does not mean it is worse. It is very similar to the
price to earnings (PE) ratio.

### `graph.py`

## How Do I Test It Out?

You are encouraged to clone this repository and try this stuff out for yourself!
This way, you will be able to use your own personal numbers. I tried to include
options for anything that made sense. If there is something missing, please
create an issue or send me an email.

### Dependencies

* [python](https://docs.python.org/3/whatsnew/3.8.html) (3.8+)
* [matplotlib](https://matplotlib.org)
* [progressbar2](https://pypi.org/project/progressbar2/)

## Rules and Assumptions

Not trying to hide this stuff, but here are some gotchas. Most of this stuff
boils down to it being very difficult to predict the future. But some things
were intential design decisions.

### Income

* There are no gaps in employment.
* Pay raises are constant (unrealistic, I'm aware).

### Taxes

* Federal taxes only; no state tax, social security, medicare, etc.
* Standard duduction only.
* Only "single" and "married" filing statuses.
* No dependents; no charities.

### RMDs

* After retirement and before RMDs, you will do [Roth IRA
  conversions](https://www.bogleheads.org/wiki/Roth_IRA_conversion). This amount
  is automatically calculated to produce the lowest taxes. Note: this currently
  assumes your marital status does not change during this
  post-retirement/pre-RMDs period. I understand that will not work for everyone.
* During RMDs, you will withdrawal at least your standard deduction. This is
  amount is taxed at 0%.
* RMDs are transferred to a taxable account, where it grows at the same interest
  rate as retirement accounts.

### Other

* Interest is applied at the end of each year.
* The "market" has no volatility. Investments grow at a steady rate.
* Divorce is not possible. Once you are married, you are stuck that way.
* Taxable investments are never sold and therefore capital gains is take taken
  into account. I could see myself adding a "yearly cost of living" option and
  intelligently withdrawing from the best account. In this situation, capital
  gains could be calculated and included.
