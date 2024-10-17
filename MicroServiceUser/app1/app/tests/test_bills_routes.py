import pytest
from unittest.mock import patch
from flask import Flask
from ..bills import init_bills
from ..core.models import Bill, Category

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
    def test_add_bills_new_bill(self, mock_create_bill, mock_auth, client):
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

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.create_bill')
    def test_add_bills_not_description(self, mock_create_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_create_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)

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

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.create_bill')
    def test_add_bills_not_user(self, mock_create_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_create_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)

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
        assert response.json["error"] == "Os campos description, valor_compra, include_date, due_date, type e usuario são obrigatórios"

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.create_bill')
    def test_add_bills_not_type(self, mock_create_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_create_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
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
        assert response.json["error"] == "Os campos description, valor_compra, include_date, due_date, type e usuario são obrigatórios"

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.create_bill')
    def test_add_bills_not_parcela(self, mock_create_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_create_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
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

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.create_bill')
    def test_add_bills_not_due_date(self, mock_create_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_create_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
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

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.create_bill')
    def test_add_bills_not_valor_compra(self, mock_create_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_create_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
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

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.create_bill')
    def test_add_bills_not_valor_compra(self, mock_create_bill, mock_auth, client):
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
        
        mock_auth.return_value = False
        response = client.post('/bills/add', json=data)
        assert response.status_code == 401
        assert response.json["error"] == "Usuário não autorizado"

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.update_bill')
    def test_update_bill_description(self, mock_update_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_update_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        data = {
            "id":1,
            "description": "Loja de Sapato", 
            "category": None,
            "valor_compra": 1000.00,
            "usuario": 1
        }
        response = client.put('/bills/update', json=data)
        assert response.status_code == 201
        assert response.json is True

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.update_bill')
    def test_update_bill_not_authorization(self, mock_update_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_update_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        data = {
            "id":1,
            "description": "Loja de Sapato", 
            "category": None,
            "valor_compra": 1000.00,
            "usuario": 1
        }
        mock_auth.return_value = False
        response = client.put('/bills/update', json=data)
        assert response.status_code == 401
        assert response.json["error"] == "Usuário não autorizado"

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.update_bill')
    def test_update_bill_not_id(self, mock_update_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_update_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        data = {
            "id":None,
            "description": "Loja de Sapato", 
            "category": None,
            "valor_compra": 1000.00,
            "usuario": 1
        }

        response = client.put('/bills/update', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Informe uma conta válida."

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.update_bill')
    def test_update_bill_not_valor_compra(self, mock_update_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_update_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        data = {
            "id":1,
            "description": "Loja de Sapato", 
            "category": None,
            "valor_compra": None,
            "usuario": 1
        }

        response = client.put('/bills/update', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Informe um valor."
    
    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.update_bill')
    def test_update_bill_not_type_compra(self, mock_update_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_update_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        data = {
            "id":1,
            "description": "Loja de Sapato", 
            "category": None,
            "valor_compra": "ABC",
            "usuario": 1
        }

        response = client.put('/bills/update', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "O valor deve ser um número"

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.update_bill')
    @patch('app.core.service.CategoryService.existe_categoria')
    def test_update_bill_category(self, mock_existe_category, mock_update_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_update_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        mock_existe_category.return_value = True
        data = {
            "id":1,
            "description": "Loja de Sapato", 
            "category": 1,
            "valor_compra": 1000.00,
            "usuario": 1
        }

        response = client.put('/bills/update', json=data)
        assert response.status_code == 201
        assert response.json is True

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.update_bill')
    @patch('app.core.service.CategoryService.existe_categoria')
    def test_update_bill_category_not_exists(self, mock_existe_category, mock_update_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_update_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        mock_existe_category.return_value = False
        data = {
            "id":1,
            "description": "Loja de Sapato", 
            "category": 1,
            "valor_compra": 1000.00,
            "usuario": 1
        }

        response = client.put('/bills/update', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Categoria não existe."

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.update_bill')
    def test_update_bill_not_bill(self, mock_update_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_update_bill.return_value = None
        data = {
            "id":2,
            "description": "Loja de Sapato", 
            "category": None,
            "valor_compra": 1000.00,
            "usuario": 1
        }

        response = client.put('/bills/update', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Conta não encontrada."

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.delete')
    @patch('app.core.service.BillService.existe_conta')
    def test_delete_bill(self, mock_existe_bill, mock_delete_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_delete_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        mock_existe_bill.return_value = True
        data = {
            "id":1,
            "usuario": 1
        }

        response = client.delete('/bills/delete', json=data)
        assert response.status_code == 200
        assert response.json["message"] == "Conta excluída com sucesso"
    
    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.delete')
    @patch('app.core.service.BillService.existe_conta')
    def test_delete_bill_not_authorized(self, mock_existe_bill, mock_delete_bill, mock_auth, client):
        mock_auth.return_value = False
        mock_delete_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        mock_existe_bill.return_value = True

        data = {
            "id":1,
            "usuario": 1
        }

        response = client.delete('/bills/delete', json=data)
        assert response.status_code == 401
        assert response.json["error"] == "Usuário não autorizado"
    
    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.delete')
    @patch('app.core.service.BillService.existe_conta')
    def test_delete_bill_not_id(self, mock_existe_bill, mock_delete_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_delete_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        mock_existe_bill.return_value = True
        data = {
            "id":None,
            "usuario": 1
        }

        response = client.delete('/bills/delete', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Informe uma conta válida."

    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.delete')
    @patch('app.core.service.BillService.existe_conta')
    def test_delete_bill_not_user(self, mock_existe_bill, mock_delete_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_delete_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        mock_existe_bill.return_value = True
        data = {
            "id":1,
            "usuario": None
        }

        response = client.delete('/bills/delete', json=data)
        assert response.status_code == 400
        assert response.json["error"] == "Informe um usuário válido."
    
    @patch('app.authorization.userAuthorization.UserAuthorization.get_autorizacao_usuario')
    @patch('app.core.service.BillService.delete')
    @patch('app.core.service.BillService.existe_conta')
    def test_delete_bill_not_exists_bill(self, mock_existe_bill, mock_delete_bill, mock_auth, client):
        mock_auth.return_value = True
        mock_delete_bill.return_value = Bill(1, "Loja de Roupa", 1000.00, "15/10/2024", "15/10/2024", 1, None, None, 1, 1000.00, None)
        mock_existe_bill.return_value = False
        data = {
            "id":1,
            "usuario": 1
        }

        response = client.delete('/bills/delete', json=data)
        assert response.status_code == 404
        assert response.json["error"] == "Conta não encontrada para o usuário."