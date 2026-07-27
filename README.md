# Portfolio Trade Service

Given a trade amount, the service apportions it across the symbols in a customer's
target portfolio by weight and returns the resulting per-symbol orders. It calculates
orders only — nothing is executed or persisted.

## Stack

| Concern | Choice |
| --- | --- |
| HTTP | `fastapi[standard]` |
| Request validation | Pydantic v2 models |
| Config | `pydantic-settings` — env vars into a typed `Settings` |
| YAML | `PyYAML` |
| API docs | FastAPI's built-in Swagger UI / ReDoc |
| Reload during development | `fastapi dev`, running inside the container |
| Storage | none — YAML loaded into memory at startup |

## Running it

```bash
make up

# or, if you don't have `make`:

docker compose up --build
```

There's no supported bare-metal workflow — `main.py` builds `Settings` at import
time and `DATA_DIR` requires `/data` to exist, which is only true inside the
container (mounted from `./data`). The API serves on
`http://localhost:${API_EXT_PORT:-8000}`.

```bash
curl -s localhost:8000/users/1/trades \
  -H 'Content-Type: application/json' \
  -d '{"amount":10000}'
```

```json
{
  "amount": 10000,
  "target_portfolio": { "A": 40, "B": 60 },
  "orders": [
    { "symbol": "A", "amount": 4000, "quantity": "4.000" },
    { "symbol": "B", "amount": 6000, "quantity": "38.709" }
  ]
}
```

Interactive docs at `http://localhost:8000/docs` (and `/redoc`). Both are disabled
when `PROD=true`.

## Business rules

- Target portfolio, stock prices, and per-stock tradability are already configured
  (`data/portfolio.yml`, `data/stocks.yml`).
- All yen calculations floor — integer division throughout, never float division on
  the way to a yen amount.
- Minimum trade amount: ¥1,000.
- The trade amount is apportioned across the target portfolio's weights: a ¥10,000
  trade against `A: 40%, B: 60%` produces `A: ¥4,000`, `B: ¥6,000`.
- A halted (non-tradable) or unknown stock is excluded, and its weight is
  redistributed across the remaining eligible symbols.
- Minimum order amount: ¥200. A symbol whose apportioned share falls below that is
  excluded and its weight redistributed the same way as a halted stock.
- Orders are placed in units of 0.001 shares — the largest quantity satisfying
  `quantity * price <= order_amount`. A symbol too expensive to buy even 0.001 of a
  share at its apportioned amount is excluded and its weight redistributed, same as
  the two rules above.
- Exclusion and redistribution run in a single pass — excluding a symbol only
  increases the survivors' shares, so no cascade back onto an already-decided symbol
  is possible.
- Flooring can leave a small remainder unallocated (e.g. a ¥10,000 trade producing
  orders totaling ¥9,999) — this is expected, not a bug.
- A portfolio referencing a ticker absent from the stock catalogue is a
  data-integrity problem, not a client error — checked at startup and surfaced as a
  500 if it ever reaches the request path.

## Folder structure

```
src/
  main.py              app factory (create_app), lifespan, exception handlers
  settings.py          pydantic-settings; get_settings() is lru_cached
  yaml_io.py           read_yaml — file I/O only, no domain knowledge
  api/
    deps.py            the whole Depends chain lives here
    routes/users.py    POST /users/{user_id}/trades
    schemas/trade.py   TradeRequest, TradeResponse
  domain/
    const.py           MIN_TRADE_AMOUNT, MIN_ORDER_AMOUNT, QUANTITY_PRECISION
    exceptions.py      PortfolioNotFound, UnknownStocksInPortfolio, TradeAmountBelowMinimum
    repositories.py    StockRepository, UserPortfolioRepository — ABCs (ports)
    models/            Stock, UserPortfolio, Order, TradeResult, Ticker
    services/
      trade_calculator.py   pure allocation logic, no I/O
  application/
    trade_service.py   orchestration: fetches via repository ports, raises
                        not-found/unknown-ticker, calls TradeCalculator, assembles
                        TradeResult
  repositories/        InMemoryStockRepository, InMemoryUserPortfolioRepository
data/
  stocks.yml
  portfolio.yml
scripts/start.sh
compose.yml
Dockerfile
Makefile
pyproject.toml
```

## Testing

```bash
make test
```

(also works against the container already running, via
`docker compose run --rm test pytest`). No bare-metal `pytest` — same `/data`
constraint as running the app.

Expected values in the calculator/service/integration tests are hand-computed, not
derived from the implementation — the point is catching a shared misunderstanding,
which computing them from the same code under test wouldn't do.

Trivial declarative models and wiring don't have dedicated unit tests — they're
exercised through whatever uses them, and have no decisions in them worth testing in
isolation.
