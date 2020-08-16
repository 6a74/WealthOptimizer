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
* Your income will grow at a steady rate.

### Taxes
* This only accounts for federal taxes. No state tax, social security, medicare,
   etc.
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
* RMDs are put into a taxable account, where it will grow at the same interest
  rate.

### Other

* Interest is applied at the end of each year.
* The "market" has no volatility. Investments will grow at a steady rate.


## Figures

![Figure 1](https://github.com/6a74/finance/blob/master/figures/Figure_20.png?raw=true)
