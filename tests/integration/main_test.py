from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import create_app
from settings import Settings


class TestRoot:
    def test_root(self, client: TestClient) -> None:
        res = client.get("/")
        assert res.status_code == 200


class TestStartupValidation:
    def test_fails_when_portfolio_references_unknown_ticker(self, tmp_path: Path) -> None:
        (tmp_path / "stocks.yml").write_text("- ticker: A\n  price: 100\n  tradable: true\n")
        (tmp_path / "portfolio.yml").write_text(
            "- user_id: 1\n  target_portfolio:\n    A: 50\n    ZZZ: 50\n"
        )
        settings = Settings(DATA_DIR=tmp_path)

        with pytest.raises(RuntimeError, match="ZZZ"):
            with TestClient(create_app(settings)):
                pass
