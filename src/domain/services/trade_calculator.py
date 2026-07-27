from domain.const import MIN_ORDER_AMOUNT, MIN_TRADE_AMOUNT, QUANTITY_PRECISION
from domain.models import Order, Stock, Ticker, UserPortfolio


class TradeCalculator:
    def calculate(
        self, portfolio: UserPortfolio, stocks: dict[Ticker, Stock], amount: int
    ) -> list[Order]:
        if amount < MIN_TRADE_AMOUNT:
            raise ValueError(f"Trade amount {amount} is below the minimum of {MIN_TRADE_AMOUNT}")

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
