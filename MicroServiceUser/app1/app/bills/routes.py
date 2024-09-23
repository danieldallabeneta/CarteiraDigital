from flask import Blueprint, jsonify, request
from .adapters import MongoBillRepository
from app.category.adapters import MongoCategoryRepository
from app.core.service import BillService, CategoryService
from datetime import datetime

bills_bp = Blueprint('bills', __name__)
bill_service = BillService(MongoBillRepository())
category_service = CategoryService(MongoCategoryRepository())

@bills_bp.route('/add', methods=['POST'])
def create_bill():
    data = request.json
    type = data.get("type")
    category = data.get("category")
    valor_compra = data.get("valor_compra")
    usuario = data.get("usuario")
    parcela = data.get("parcela")
    required_fields = ["description", "valor_compra", "include_date", "due_date","type", "usuario"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Os campos description, valor_compra, include_date, due_date, type e usuario são obrigatórios"}), 400

    if usuario is None:
        return jsonify({"error": "Informe um usuário responsável."}), 400

    if type is None:
        return jsonify({"error": "Informe se a conta é Parcelada ou à vista."}), 400

    if type == 2:
        if parcela is None:
            return jsonify({"error": "Para as contas parceladas, é necessário informar a quantidade de parcela."}), 400
        if data.get("due_date") is None:
            return jsonify({"error": "Informe uma data de vencimento."}), 400

    if category != None:
        b_existe_categoria = category_service.existe_categoria(category, usuario)
        if b_existe_categoria == False:
            return jsonify({"error": "Categoria não existe."}), 400
    
    if valor_compra is None:
        return jsonify({"error": "Informe o valor da conta."}), 400

    bill = bill_service.create_bill(data)
    return jsonify(True) if bill else jsonify(False), 201

@bills_bp.route('/update', methods=['PUT'])
def update_bill():
    data = request.json
    id = data.get('id')
    description = data.get('description')
    category = data.get('category')
    valor_compra = data.get('valor_compra')
    usuario = data.get('usuario')

    if id is None:
        return jsonify({"error": "Informe uma conta válida."}), 400

    if valor_compra is None:
        return jsonify({"error": "Informe um valor."}), 400
    
    try:
        valor = float(valor_compra)
    except ValueError:
        return jsonify({'error': 'O valor deve ser um número'}), 400
    
    if category != None:
        b_existe_categoria = category_service.existe_categoria(category, usuario)
        if b_existe_categoria == False:
            return jsonify({"error": "Categoria não existe."}), 400

    bill_data = bill_service.update_bill(id,description,category,valor,usuario)
    if not bill_data:
        return jsonify({"error": "Conta não encontrada."}), 400
    return jsonify(True), 201

@bills_bp.route('/delete', methods=['DELETE'])
def delete_bill():
    data = request.json
    id   = data.get('id')
    usuario = data.get('usuario')

    if id is None:
        return jsonify({"error": "Informe uma conta válida."}), 400
    
    if usuario is None:
        return jsonify({"error": "Informe um usuário válido."}), 400

    b_existe_conta = bill_service.existe_conta(id, usuario)
    if not b_existe_conta:
        return jsonify({"erro": "Conta não encontrada para o usuário."}), 404

    result = bill_service.delete(id)
    if not result:
        return jsonify({'error': 'Conta não encontrada'}), 404

    if result.deleted_count > 0:
        return jsonify({'message': 'Conta excluída com sucesso'}), 200
    else:
        return jsonify({'error': 'Conta não encontrada'}), 404

@bills_bp.route('/all', methods=['GET'])
def get_all_by_user():
    usuario = request.args.get('usuario')

    if usuario is None:
        return jsonify({'error': 'Parâmetro de usuário é obrigatório'}), 400

    try:
        # Convertendo o parâmetro para inteiro
        usuario = int(usuario)
    except ValueError:
        return jsonify({'error': 'O parâmetro de usuário deve ser um inteiro'}), 400

    results = bill_service.get_all_by_user_id(usuario)

    results_list = [{'id': str(doc['bill']), 'nome': doc['description'],'valor_compra': doc['valor_compra'],'data_inclusao': doc['include_date'].strftime("%d/%m/%Y"), 
                     'vencimento': doc['due_date'].strftime("%d/%m/%Y"),'forma_pagamento': "Parcelado" if doc['type'] == 2 else "À Vista",'parcelas': 0 if doc['type'] == 1 else doc['parcela'],
                     'usuario': doc['usuario'], 'valor_parcela': doc['valor_parcela'], 'parcela_paga':doc['parcela_paga']} for doc in results]
    
    if results_list:
        return jsonify(results_list), 200
    else:
        return jsonify({'message': 'Nenhum registro encontrado para o usuário fornecido'}), 404

