"""Базовые функции и фикстуры для работы Pytest"""
from pytest import fixture

from fastapi.testclient import TestClient

from app.main import app


@fixture(scope='session')
def api() -> TestClient:
    return TestClient(app)
