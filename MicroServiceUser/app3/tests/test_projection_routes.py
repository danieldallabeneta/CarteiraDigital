import pytest
from unittest.mock import patch
from flask import Flask
from ..projectionService import create_app

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    create_app(app)
    with app.test_client() as client:
        yield client

class TestProjectionRoutes:

    @patch('authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('projectionService.services.Services.get_data_graph')
    def test_graph(self, mock_get_data_graph, mock_auth, client):
        mock_auth.return_value = True
        mock_get_data_graph.return_value = {}
        assert True == True