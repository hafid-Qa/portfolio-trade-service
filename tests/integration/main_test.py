from fastapi.testclient import TestClient


class RootTest:
    def test_root(self, client: TestClient) -> None:
        res = client.get("/")
        assert res.status_code == 200
