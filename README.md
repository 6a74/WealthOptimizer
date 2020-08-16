# When to Start Deferring Taxes?

Many people on [Bogleheads](https://www.bogleheads.org), a fantastic resource
for investing advice, believe that it is almost always better to defer taxes
(_i.e._ contribute to
[Traditional](https://www.bogleheads.org/wiki/Traditional_IRA) accounts rather
than [Roth](https://www.bogleheads.org/wiki/Roth_IRA) accounts). I would like to
make the case against Traditional accounts, especially for young people. To help
myself, I have developed a set of utilities to demonstrate what I mean.

My core argument is based around [minimum required
distributions](https://www.bogleheads.org/wiki/Required_Minimum_Distribution)
(RMD). As the name suggests, these are IRS-mandated withdrawals from select
retirement accounts. If an investor puts too much money in tax-deferred
accounts, they might be forced to withdrawal large sums of money, which could be
heavily taxed. The alternative is to redirect those contributions to Roth
accounts, in which you pay taxes up-front and then (hopefully) never again.

## Rules and Assumptions

### Income

* There are no gaps in employment.
* Pay raises are steady (`--yearly-income-raise`).

### Taxes
* Federal taxes only; no state tax, social security, medicare, etc.
* Standard duduction is assumed.
* Dependents are not taken into account.
* Only "single" and "married" are options.

### RMDs

* After retirement and before RMDs, you will do [Roth IRA
  conversions](https://www.bogleheads.org/wiki/Roth_IRA_conversion). This amount
  is automatically calculated to produce the lowest taxes. Note: this currently
  assumes your marital status does not change during this
  post-retirement/pre-RMDs period. I understand that will not work for everyone.
* During RMDs, you will withdrawal at least your standard deduction. This is
  amount is taxed at 0%.
* RMDs transferred to a taxable account, where it will grow at the same interest
  rate as retirement accounts.

### Other

* Interest is applied at the end of each year.
* The "market" has no volatility. Investments will grow at a steady rate.
* Divorce is not possible. Once you are married, you are stuck that way.


## Figures

Note: In most figures, after a certain number of years, the tax rate grows at a
constant rate. This is due to there being so little in Traditional
(tax-deferred) accounts. RMDs are relativly small (less than your standard
deduction) and taxed generally taxed near (or at) 0%. After this point, it
becomes clearily detremental to not defer taxes.

The figure below shows a 20 year old with nothing in retirement:

![Figure 1](https://github.com/6a74/finance/blob/master/figures/Figure_20.png?raw=true)

The figure below shows a 25 year old with nothing in retirement:

![Figure 2](https://github.com/6a74/finance/blob/master/figures/Figure_25.png?raw=true)

The figure below shows a 40 year old with nothing in retirement:

![Figure 3](https://github.com/6a74/finance/blob/master/figures/Figure_40.png?raw=true)

This figure shows what values looks like without scaling:

![Figure 4](https://github.com/6a74/finance/blob/master/figures/Figure_20_noscale.png?raw=true)

The figure below shows a 20 year old that retires 10 years earlier (at 50):

![Figure 5](https://github.com/6a74/finance/blob/master/figures/Figure_20_retire_at_50.png?raw=true)

The figure below shows a 20 year old that retires 20 years earlier (at 40):

![Figure 6](https://github.com/6a74/finance/blob/master/figures/Figure_20_retire_at_40.png?raw=true)
