import pytest
from unittest.mock import patch
from flask import Flask
import os
from ..category import init_category
from..core.models import Category

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    init_category(app)
    with app.test_client() as client:
        yield client

class TestCategoryRoutes:

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.CategoryService.create_category')
    def test_add_category(self, mock_create_category, mock_auth, client):
        print(os.path.exists('/app1/app/category/category_documentation.yml'))
        mock_auth.return_value = True
        mock_create_category.return_value = Category(category=1, name="Categoria Teste", usuario=1)

        data = {
            "name": "Categoria Teste",
            "usuario": 1
        }

        response = client.post('/category/add', json=data)
        assert response.status_code == 201
        assert response.json['message'] == "Registro inserido com sucesso"

        response = client.post('/category/add', json={"name": "Categoria Teste"})
        assert response.status_code == 400
        assert response.json["error"] == "Todos os campos (nome, usuario) são obrigatórios"

        mock_auth.return_value = False
        response = client.post('/category/add', json=data)
        assert response.status_code == 401
        assert response.json["error"] == "Usuário não autorizado"
