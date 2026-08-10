from fastapi import status
from fastapi.testclient import TestClient

from api.schemas import TradeResponse


class TestUserTrades:
    def test_apportions_by_target_weight(self, client: TestClient) -> None:
        res = client.post("/users/1/trades", json={"amount": 10000})

        assert res.status_code == status.HTTP_200_OK
        payload = res.json()
        assert TradeResponse.model_validate(payload)
        assert payload == {
            "amount": 10000,
            "target_portfolio": {"A": 40, "B": 60},
            "orders": [
                {"symbol": "A", "amount": 4000, "quantity": "4.000"},
                {"symbol": "B", "amount": 6000, "quantity": "38.709"},
            ],
        }

    def test_excludes_untradable_symbol(self, client: TestClient) -> None:
        res = client.post("/users/2/trades", json={"amount": 10000})

        assert res.status_code == status.HTTP_200_OK
        payload = res.json()
        assert TradeResponse.model_validate(payload)
        assert payload == {
            "amount": 10000,
            "target_portfolio": {"E": 100},
            "orders": [],
        }

    def test_reapportions_after_excluding_untradable_symbol(self, client: TestClient) -> None:
        res = client.post("/users/3/trades", json={"amount": 10000})

        assert res.status_code == status.HTTP_200_OK
        payload = res.json()
        assert TradeResponse.model_validate(payload)
        assert payload["target_portfolio"] == {"A": 31, "B": 40, "E": 29}
        assert payload["orders"] == [
            {"symbol": "A", "amount": 4366, "quantity": "4.366"},
            {"symbol": "B", "amount": 5633, "quantity": "36.341"},
        ]

    def test_excludes_below_minimum_order_amount_and_reapportions(self, client: TestClient) -> None:
        res = client.post("/users/4/trades", json={"amount": 1000})

        assert res.status_code == status.HTTP_200_OK
        payload = res.json()
        assert TradeResponse.model_validate(payload)
        assert payload["target_portfolio"] == {"B": 50, "C": 49, "D": 1}
        assert payload["orders"] == [
            {"symbol": "B", "amount": 505, "quantity": "3.258"},
            {"symbol": "C", "amount": 494, "quantity": "0.222"},
        ]

    def test_reapportions_after_excluding_order_that_floors_to_zero_quantity(
        self, client_with: TestClient
    ) -> None:
        res = client_with.post("/users/5/trades", json={"amount": 10000})

        assert res.status_code == status.HTTP_200_OK
        payload = res.json()
        assert TradeResponse.model_validate(payload)
        assert payload["target_portfolio"] == {"A": 98, "X": 2}
        assert payload["orders"] == [{"symbol": "A", "amount": 10000, "quantity": "10.000"}]

    def test_errors_when_portfolio_references_unknown_stock(self, client_with: TestClient) -> None:
        res = client_with.post("/users/6/trades", json={"amount": 10000})

        assert res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res.json() == {"detail": "internal error"}

    def test_returns_404_for_unknown_user(self, client: TestClient) -> None:
        res = client.post("/users/999/trades", json={"amount": 10000})

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_rejects_amount_below_minimum_trade_amount(self, client: TestClient) -> None:
        res = client.post("/users/1/trades", json={"amount": 500})

        assert res.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
