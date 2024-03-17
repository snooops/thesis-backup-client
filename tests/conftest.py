import pytest
from backupclient import create_app


@pytest.fixture
def app():
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()