# Wealth Optimizer

This repository contains utilities that will help you maximize your wealth and
pay less in taxes. The core componenent is a financial simulator that simulates
every year of your life. It will contribute to accounts in the most tax-efficent
order. And during retirement, it will withdrawal from the most tax-efficent
accounts.

## Dependencies

* [python](https://docs.python.org/3/whatsnew/3.8.html) (3.8+)
* [matplotlib](https://matplotlib.org)
* [rich](https://pypi.org/project/rich/)

## Rules and Assumptions

Not trying to hide this stuff, but here are some gotchas. Most of this stuff
boils down to it being very difficult to predict the future. But some things
were intential design decisions.

### Income

* There are no gaps in employment.
* Pay raises are constant (unrealistic, I'm aware).
* Any excess income will go into a taxable account.

### Required Minimum Distributions (RMDs)

* After retirement and before RMDs, you will do [Roth IRA
  conversions](https://www.bogleheads.org/wiki/Roth_IRA_conversion). This amount
  is automatically calculated to produce the highest assets at death. Note: this
  currently assumes your marital status does not change during this
  post-retirement/pre-RMDs period. I understand that this will not work for
  everyone.
* During RMDs, you will withdrawal at least your standard deduction. This is
  amount is taxed at 0%.
* Excess RMDs are transferred to a taxable account, where it grows at the same
  interest rate as retirement accounts.

### Taxes

* Standard duduction only.
* Only "single" and "married" filing statuses.
* If there are traditional investments at death, it assumes that one of your
  children will inherit the remainder. Your child will be 30 years younger than
  your age of death. They will be expected to take RMDs based on the IRS Single
  Life Expectancy table. The taxes they expect to pay for this will be included
  in your total taxes. Assuming your child has no income for the remainder of
  their life, this will be the minimum expected tax.
* Outside of estate taxes, there are no taxes for taxable and Roth investments
  at death. For taxable accounts, the [step up in
  basis](https://www.investopedia.com/terms/s/stepupinbasis.asp) plays a
  significant role in helping to reduce taxes after death.

### Other

* Interest is applied at the end of each year.
* The "market" has no volatility. Investments grow at a steady rate.
* Divorce is not possible. Once you are married, you are stuck that way.
* Spending remains constant thoughout your lifetime. Once again, this is
  unrealistic but necessary. Because interest rates are real, this number
  accounts for inflation.

## Utilities

### `sim.py`

Given all of the initial variables (parameters), this script will simulate
your portfolio and show you each year of your life. Running the following
command will produce the graph below:

```
./source/sim.py
```

![Sim](https://github.com/6a74/WealthOptimizer/blob/master/figures/sim_01.png?raw=true)

A simulation with more options, like this:

```
./source/sim.py \
--current-age=25 \
--income=100000 \
--starting-balance-trad-401k=100000 \
--max-contribution-percentage-401k=0.50 \
--employer-match-401k=0.07 \
--employer-contribution-hsa=750
--do-mega-backdoor-roth \
```

Will look like this:

![Sim2](https://github.com/6a74/WealthOptimizer/blob/master/figures/sim_02.png?raw=true)

### `graph.py`

The `graph.py` utility is meant to help you determine how long to wait before
start deferring taxes via pre-tax contributions, rather than Roth contributions.
The lines represent your total assets (estate) after taxes at death. The goal is
to maximize this value. The higher (vertically) the line the better. It should
be noted that lines (interest rates) are independent from one another. The total
assets will be vary widely between different interest rates. The lines are
normalized to fit between 0.0 and 1.0 so they can be easily compared.

```
./source/graph.py
```

![Figure 1](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_01.png?raw=true)

#### Example Scenarios

The figure below shows the typical American. They make a little more than
$60k/year. Unlike the typical American though, they max out their retirement
accounts each year. This figure shows that if you expect the long-term real
interest rate to be 6% or higher, you might be better off making Roth
contributions for a few years.

![Figure 1](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_01.png?raw=true)

Though, if the same person in the figure above were to have $100k already saved
in their traditional retirement accounts, the outcome would be quite different.
The (relatively) small amount grows exponentially and requires higher RMDs.

![Figure 2](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_02.png?raw=true)

Next, we have a slightly younger person, 25, that is just starting their career.
They have nothing in their retirement, but they graduated without debt and got a
decent job out of college making approximately $63k/year (what the typical
American makes). With long-term interest rates of 5%, 6%, and 7% this person
should prefer Roth contributions for at least the first decade of their career.
Note: for all of the figures with a starting age of 25, the little upticks at
year 5 are a result of becoming married. Due to better tax rates, you will pay
less in taxes and invest more.

![Figure 3](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_03.png?raw=true)

Say the same recent graduate got a job making $100k/year instead of $63k/year.
What would change? Well, because of their higher income, traditional IRA
contributions are not deductible. There is no point in contributing to a
non-deductible IRA. Instead, they would contribute to a Roth IRA. For this
reason, it appears that this person would get less out of Roth contributions
than the previous lad.

![Figure 4](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_04.png?raw=true)

Next, let's say the person above has a coworker that is the same age and has the
same income, _but_ spends twice as much (from $30k to $60k). What would change?
Well, not much honestly. Their tax-advantaged savings should be on par, just
their taxable savings would be different.

![Figure 5](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_05.png?raw=true)

Next, assume one of these lads were real lucky and got an internship at a nice
company during college, and somehow they found a way to sock away $100k into
their traditional retirement accounts. This definitely pushes the scale towards
Roth contributions for the beginning of their career.

![Figure 6](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_06.png?raw=true)

Let's jump back to the new-grad making $63k/year, but say this person really wants to
retire early, say at 50 years old instead of 60. Unless their investments can
provide a 7% real return, they will probably be better off purely contributing
to traditional retirement accounts.

![Figure 7](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_07.png?raw=true)

On the other hand, what happens if this person decides to work a little bit
longer, till the age of 70. Will this change things? By golly, it will. Unless
their investments do very poorly over a long time, this person will be better
off starting with Roth contributions.

![Figure 8](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_08.png?raw=true)

Next, let's say there's a hot-shot kid in Silicon Valley making $300/year and
they want to retire at 40. Because they will have so few years in the workforce,
traditional contributions will not make much of a difference in terms of RMDs.
And because of their very high income, tax deductions are very valuable. These
deductions do more good than RMDs do bad.

![Figure 9](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_09.png?raw=true)

Let's say the same hot-shot kid decides he likes his job and wants to work
another twenty years. The outcome is still the same. This person should always
defer taxes. Their tax-rate is too high not to.

![Figure 10](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_10.png?raw=true)

What if there is a kid who's income explodes (from $63k to $300k at a rate of
20% increases each year) while they are young? This person would reach an income
of $300k at the age of 34, then plateau. This person should immediately start
deferring taxes.

![Figure 11](https://github.com/6a74/WealthOptimizer/blob/master/figures/figure_11.png?raw=true)
