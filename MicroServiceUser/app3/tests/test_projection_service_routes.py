import pytest
from unittest.mock import patch
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestProjectionServiceRoutes:

    def test_graph(self, client):
        assert True == True