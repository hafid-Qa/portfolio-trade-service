import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import create_app
from settings import get_settings


@pytest.fixture
def client():
    test_app: FastAPI = create_app(get_settings())

    yield TestClient(test_app)
