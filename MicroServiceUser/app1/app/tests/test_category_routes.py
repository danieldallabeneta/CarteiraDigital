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

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.CategoryService.get_category_by_id')
    @patch('app.core.service.CategoryService.update_category')
    def test_update_category(self, mock_update_category, mock_get_category_by_id, mock_auth, client):
        print(os.path.exists('/app1/app/category/category_documentation.yml'))

        category_obj = Category(category=1, name="Categoria Antiga", usuario=1)

        mock_get_category_by_id.return_value = category_obj.to_dict()
        mock_auth.return_value = True
        mock_update_category.return_value = Category(category=1, name="Categoria Atualizada", usuario=1)

        data = {
            "id": 1,
            "name": "Categoria Atualizada"
        }

        response = client.put('/category/update_category', json=data)
        assert response.status_code == 201
        assert response.json["sucesso"] == "Categoria Atualizada."

        response = client.put('/category/update_category', json={"id": 1})
        assert response.status_code == 400
        assert response.json["error"] == "Os campos de id e name são obrigatórios."

        mock_auth.return_value = False
        response = client.put('/category/update_category', json=data)
        assert response.status_code == 401
        assert response.json["error"] == "Usuário não autorizado."

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.CategoryService.get_all_for_user')
    def test_get_all_category(self, mock_get_all_for_user, mock_auth, client):
        mock_auth.return_value = True
        mock_get_all_for_user.return_value = [
            Category(category=1, name="Categoria 1", usuario=1).to_dict(),
            Category(category=2, name="Categoria 2", usuario=1).to_dict()
        ]

        response = client.get('/category/get_all?usuario=1')
        assert response.status_code == 200
        assert len(response.json) == 2

        response = client.get('/category/get_all')
        assert response.status_code == 400
        assert response.json["error"] == "Parâmetro de usuário é obrigatório."

        mock_auth.return_value = False
        response = client.get('/category/get_all?usuario=1')
        assert response.status_code == 401
        assert response.json["error"] == "Usuário não autorizado."
