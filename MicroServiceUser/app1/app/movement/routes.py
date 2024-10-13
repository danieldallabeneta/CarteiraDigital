from flask import Blueprint, jsonify, request
from .adapters import MongoMovementRepository
from app.wallet.adapters import MongoWalletRepository
from app.core.service import MovementService, WalletService
from app.authorization.userAuthorization import UserAuthorization

movement_bp = Blueprint('movement', __name__)
movement_service = MovementService(MongoMovementRepository())
user_authorization = UserAuthorization()
wallet_service = WalletService(MongoWalletRepository())

@movement_bp.route('/get_all', methods=['GET'])
def get_all_movemets():
    usuario = request.args.get('usuario')
    if usuario is None:
        return jsonify({'error': 'Parâmetro de usuário é obrigatório'}), 400    
    try:
        usuario = int(usuario)
    except ValueError:
        return jsonify({'error': 'O parâmetro de usuário deve ser um inteiro'}), 400
    
    valido = user_authorization.get_autorizacao_usuario(usuario)
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401
    
    results = movement_service.get_all_by_user_id(usuario)

    results_list = [{'tipo': str(doc['type']), 'data': doc['date'], 'valor': doc['value'],'usuario': doc['usuario']} for doc in results]

    if results_list:
        return jsonify(results_list), 200
    else:
        return jsonify({'message': 'Nenhum registro encontrado para o usuário fornecido'}), 404

@movement_bp.route('/get', methods=['GET'])
def get_all_movement_wallet():
    wallet = request.args.get('wallet')
    if wallet is None:
        return jsonify({'error': 'Parâmetro wallet obrigatório'}), 400    
    try:
        wallet = int(wallet)
    except ValueError:
        return jsonify({'error': 'O parâmetro wallet deve ser um valor inteiro'}), 400
    
    wallet_origem = wallet_service.get_wallet_by_id(wallet_service)

    if wallet_origem:
        valido = user_authorization.get_autorizacao_usuario(wallet_origem['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado"}), 401
    else:
         return jsonify({'error': 'Carteira não encontrada.'}), 404
    
    results = movement_service.get_all_by_id_wallet(wallet)

    results_list = [{'tipo': str(doc['type']), 'data': doc['date'], 'valor': doc['value'],'usuario': doc['usuario']} for doc in results]

    if results_list:
        return jsonify(results_list), 200
    else:
        return jsonify({'message': 'Nenhum movimento encontrado'}), 404