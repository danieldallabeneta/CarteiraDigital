import pytest
from unittest.mock import patch
from flask import Flask
from ..bills import init_bills
from..core.models import Bill


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    init_bills(app)
    with app.test_client() as client:
        yield client

class TestBillsRoutes:

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.create_bill')
    def test_add_bills(self, mock_create_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_create_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)

        data = {
            "description": "Loja de Roupa", 
            "valor_compra": 1000.00, 
            "include_date":"15/10/2024", 
            "due_date":"15/10/2024", 
            "type": 1, 
            "parcela": None, 
            "category": None, 
            "usuario": 1, 
            "valor_parcela": 1000.00, 
            "parcela_paga":None
        }

        response = client.post('/bills/add', json=data)
        assert response.status_code == 201
        assert response.json is True

        data_not = {
            "valor_compra": 1000.00, 
            "include_date":"15/10/2024", 
            "due_date":"15/10/2024", 
            "type": 1, 
            "parcela": 1, 
            "category": 1, 
            "usuario": 1, 
            "valor_parcela": 1000.00, 
            "parcela_paga":0
        }

        response = client.post('/bills/add', json=data_not)
        assert response.status_code == 400
        assert response.json["error"] == "Os campos description, valor_compra, include_date, due_date, type e usuario são obrigatórios"

        data_not = {
            "description": "Loja de Roupa", 
            "valor_compra": 1000.00, 
            "include_date":"15/10/2024", 
            "due_date":"15/10/2024", 
            "type": 1, 
            "parcela": 1, 
            "category": 1, 
            "valor_parcela": 1000.00, 
            "parcela_paga":0
        }

        response = client.post('/bills/add', json=data_not)
        assert response.status_code == 400
        assert response.json["error"] == "Informe um usuário responsável."

        data_not = {
            "description": "Loja de Roupa", 
            "valor_compra": 1000.00, 
            "include_date":"15/10/2024", 
            "due_date":"15/10/2024", 
            "parcela": 1, 
            "category": 1,              
            "usuario": 1, 
            "valor_parcela": 1000.00, 
            "parcela_paga":0
        }

        response = client.post('/bills/add', json=data_not)
        assert response.status_code == 400
        assert response.json["error"] == "Informe se a conta é Parcelada ou à vista."

        data = {
            "description": "Loja de Roupa", 
            "valor_compra": 1000.00, 
            "include_date":"15/10/2024", 
            "due_date":"15/10/2024", 
            "type": 2, 
            "parcela": None, 
            "category": 1, 
            "usuario": 1, 
            "valor_parcela": 1000.00, 
            "parcela_paga":None
        }

        response = client.post('/bills/add', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Para as contas parceladas, é necessário informar a quantidade de parcela."

        data = {
            "description": "Loja de Roupa", 
            "valor_compra": 1000.00, 
            "include_date":"15/10/2024", 
            "due_date":None, 
            "type": 2, 
            "parcela": 1, 
            "category": None, 
            "usuario": 1, 
            "valor_parcela": 1000.00, 
            "parcela_paga":None
        }

        response = client.post('/bills/add', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Informe uma data de vencimento."

        data = {
            "description": "Loja de Roupa", 
            "valor_compra": None, 
            "include_date":"15/10/2024", 
            "due_date":"15/10/2024", 
            "type": 1, 
            "parcela": None, 
            "category": 1, 
            "usuario": 1, 
            "valor_parcela": 1000.00, 
            "parcela_paga":None
        }

        response = client.post('/bills/add', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Informe o valor da conta."

        mock_auth.return_value = False
        response = client.post('/bills/add', json=data)
        assert response.status_code == 401
        assert response.json["error"] == "Usuário não autorizado"