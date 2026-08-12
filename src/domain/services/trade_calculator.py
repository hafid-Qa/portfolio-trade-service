from pydantic import PositiveInt

from domain.const import MIN_ORDER_AMOUNT, MIN_TRADE_AMOUNT, QUANTITY_PRECISION
from domain.exceptions import TradeAmountBelowMinimum
from domain.models import Order, Stock, Ticker, UserPortfolio


class TradeCalculator:
    def calculate(
        self, portfolio: UserPortfolio, stocks: dict[Ticker, Stock], amount: int
    ) -> list[Order]:
        """Apportion a trade amount across a portfolio's stocks into per-symbol orders.

        Three phases:

        1. Untradable removal. A stock that is missing from the catalogue or halted can
           never receive an order, so it is removed from the eligible set *before*
           anything is apportioned. It must not appear in the denominator either: a
           halted stock holding a large weight would otherwise shrink every other
           symbol's share and could push tradable symbols below MIN_ORDER_AMOUNT.

        2. Convergence. Apportion `amount` across the eligible set, weighted by each
           ticker's ratio over the sum of eligible ratios, and drop any ticker whose
           resulting order is not placeable — either below MIN_ORDER_AMOUNT, or so
           expensive that its quantity_units floors to zero. Repeat until the set stops
           changing, so that the weight freed by a dropped ticker is always
           redistributed rather than silently lost.

           This terminates. Removing a ticker lowers `ratio_sum`, which raises every
           survivor's order amount, which in turn raises its quantity_units. No survivor
           can be pushed below a threshold by another's removal, so the set shrinks
           monotonically and settles after at most one extra pass.

        3. Construction. Build one Order per surviving ticker from the stable set.

        All yen arithmetic multiplies before dividing, and `quantity_units` stays an
        integer count through this whole layer — no float ever appears here. Dividing
        by QUANTITY_PRECISION to place the decimal point is the API schema's job.

        Args:
            portfolio: The user's target portfolio (ticker -> weight, summing to 100).
            stocks: Stock lookup for the tickers in `portfolio.target_portfolio`.
            amount: Total yen to invest. Already validated as >= MIN_TRADE_AMOUNT by the
                API schema; the check below guards direct callers of the domain layer.

        Returns:
            One Order per ticker that survived, in `portfolio.target_portfolio`
            iteration order. Empty if no ticker can be ordered.

        Raises:
            TradeAmountBelowMinimum: If `amount` is below MIN_TRADE_AMOUNT.
        """
        if amount < MIN_TRADE_AMOUNT:
            raise TradeAmountBelowMinimum(amount, MIN_TRADE_AMOUNT)

        weights: dict[Ticker, PositiveInt] = portfolio.target_portfolio

        eligible: list[Ticker] = [t for t in weights if t in stocks and stocks[t].tradable]
        ratio_sum = 0
        while eligible:
            ratio_sum = sum(weights[t] for t in eligible)
            survivors: list[Ticker] = [
                t
                for t in eligible
                if self._is_orderable(weights[t], amount, ratio_sum, stocks[t].price)
            ]
            if len(survivors) == len(eligible):
                break
            eligible = survivors

        if not eligible:
            return []

        return [
            Order(
                symbol=ticker,
                amount=(order_amount := self._order_amount(weights[ticker], amount, ratio_sum)),
                quantity_units=self._quantity_units(order_amount, stocks[ticker].price),
            )
            for ticker in eligible
        ]

    @staticmethod
    def _order_amount(ratio: int, amount: int, ratio_sum: int) -> int:
        """Yen allocated to one ticker, floored. Integer-only by construction."""
        return (ratio * amount) // ratio_sum

    @staticmethod
    def _quantity_units(order_amount: int, price: int) -> int:
        """Largest count of 1/QUANTITY_PRECISION-unit shares whose cost fits within order_amount.

        Stays an integer count of units all the way through the domain layer; the API
        schema is the one place that divides by QUANTITY_PRECISION to place the decimal
        point, so no float ever appears in this arithmetic.
        """
        return (order_amount * QUANTITY_PRECISION) // price

    def _is_orderable(self, ratio: int, amount: int, ratio_sum: int, price: int) -> bool:
        """Whether this ticker's share produces an order that can actually be placed."""
        order_amount = self._order_amount(ratio, amount, ratio_sum)
        if order_amount < MIN_ORDER_AMOUNT:
            return False
        return self._quantity_units(order_amount, price) > 0
