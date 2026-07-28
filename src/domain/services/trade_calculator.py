from domain.const import MIN_ORDER_AMOUNT, MIN_TRADE_AMOUNT, QUANTITY_PRECISION
from domain.exceptions import TradeAmountBelowMinimum
from domain.models import Order, Stock, Ticker, UserPortfolio


class TradeCalculator:
    def calculate(
        self, portfolio: UserPortfolio, stocks: dict[Ticker, Stock], amount: int
    ) -> list[Order]:
        """Apportion a trade amount across a portfolio's stocks into per-symbol orders.

        Two passes over the target portfolio:

        1. Eligibility: for each ticker, apportion `amount` by its *original* weight
           (`amount * ratio // 100`, floored). A ticker is dropped if its stock is
           missing/not tradable, or if that apportioned amount is below
           `MIN_ORDER_AMOUNT`. Only the remaining (eligible) tickers' ratios are
           summed into `ratio_sum`.
        2. Re-apportionment: `amount` is split again, this time only across the
           eligible tickers, weighted by their ratio relative to `ratio_sum`
           (`current_ratio * amount // ratio_sum`, floored) so the amount dropped
           by excluded tickers is redistributed among the rest. For each resulting
           order amount, the quantity is the largest multiple of 0.001 whose cost
           does not exceed it (`order_amount * QUANTITY_PRECISION // stock_price`,
           floored, then scaled back down). Tickers whose quantity floors to 0 are
           also dropped, since a zero-quantity order is meaningless.

        Args:
            portfolio: The user's target portfolio (ticker -> weight, summing to 100).
            stocks: Stock lookup for every ticker in `portfolio.target_portfolio`.
            amount: Total yen amount to invest, already validated as >= MIN_TRADE_AMOUNT
                by the API schema; the check below is a defensive second line.

        Returns:
            One `Order` per ticker that survived both eligibility and quantity
            exclusion, in `portfolio.target_portfolio` iteration order.

        Raises:
            TradeAmountBelowMinimum: If `amount` is below `MIN_TRADE_AMOUNT`.
        """
        if amount < MIN_TRADE_AMOUNT:
            raise TradeAmountBelowMinimum(amount, MIN_TRADE_AMOUNT)

        valid_tickers: list[Ticker] = []
        ratio_sum: int = 0
        target_portfolio = portfolio.target_portfolio
        for ticker, ratio in target_portfolio.items():
            stock = stocks.get(ticker)
            if stock is None or not stock.tradable:
                continue
            stock_value = (amount * ratio) // 100
            if stock_value >= MIN_ORDER_AMOUNT:
                valid_tickers.append(ticker)
                ratio_sum += ratio
        orders: list[Order] = []
        for ticker in valid_tickers:
            current_ratio = target_portfolio[ticker]
            order_amount = (current_ratio * amount) // ratio_sum
            stock_price = stocks[ticker].price
            quantity = (order_amount * QUANTITY_PRECISION) // stock_price / QUANTITY_PRECISION
            if quantity == 0:
                continue
            orders.append(Order(symbol=ticker, amount=order_amount, quantity=quantity))
        return orders
