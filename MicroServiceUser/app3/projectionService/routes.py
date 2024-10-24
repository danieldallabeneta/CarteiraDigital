from flask import Blueprint, jsonify, request
from .services import Services
from authorization.userAuthorization import UserAuthorization

auxiliar_bp = Blueprint('aux', __name__)
services = Services()
user_authorization = UserAuthorization()

@auxiliar_bp.route('/projections', methods=['GET'])
def projections():
    user = request.args.get('usuario')
    valido = user_authorization.get_autorizacao_usuario(user)
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401

    projections = services.generate_projections(user)
    return jsonify(projections),200

@auxiliar_bp.route('/graph', methods=['GET'])
def graph():
    wallet = request.args.get('wallet')
    data = services.get_data_graph(wallet)
    return jsonify(data),200
