from flask import Blueprint, jsonify, request
from .adapters import MongoCategoryRepository
from app.core.service import CategoryService

category_bp = Blueprint('category', __name__)
category_service = CategoryService(MongoCategoryRepository())

@category_bp.route('/add', methods=['POST'])
def add_category():
    data = request.json
    
    required_fields = ["name", "usuario"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Todos os campos (nome, usuario) são obrigatórios"}), 400

    category = category_service.create_category(data)

    return jsonify(True) if category else jsonify(False), 201

@category_bp.route('/update_category', methods=['PUT'])
def update_category():
    data = request.json
    category= data.get('id')
    new_name = data.get('name')
    if category is None or new_name is None:
        return jsonify({'error': 'Os campos de id e name são obrigatórios'}), 400

    category_data = category_service.update_category(category,new_name)

    return jsonify(True) if category_data else jsonify(False), 201

@category_bp.route('/delete/<string:category>', methods=['DELETE'])
def delete_category(category):
    result = category_service.delete(category)
    
    if not result:
        return jsonify({'error': 'Carteira não encontrada'}), 404

    if result.deleted_count > 0:
        return jsonify({'message': 'Carteira excluída com sucesso'}), 200
    else:
        return jsonify({'error': 'Carteira não encontrada'}), 404

@category_bp.route('/get_all', methods=['GET'])
def get_all_category():
    # Obtendo o valor do parâmetro 'usuario' da URL
    usuario = request.args.get('usuario')
    
    # Validar o parâmetro
    if usuario is None:
        return jsonify({'error': 'Parâmetro de usuário é obrigatório'}), 400
    
    try:
        # Convertendo o parâmetro para inteiro
        usuario = int(usuario)
    except ValueError:
        return jsonify({'error': 'O parâmetro de usuário deve ser um inteiro'}), 400
    
    results = category_service.get_all_for_user(usuario)
    
    results_list = [{'id': str(doc['category']), 'nome': doc['name'], 'usuario': doc['usuario']} for doc in results]
    
    if results_list:
        return jsonify(results_list), 200
    else:
        return jsonify({'message': 'Nenhum registro encontrado para o usuário fornecido'}), 404





    




