from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .services import Services
from authorization.userAuthorization import UserAuthorization

auxiliar_bp = Blueprint('aux', __name__)
services = Services()
user_authorization = UserAuthorization()

@auxiliar_bp.route('/projections', methods=['GET'])
@swag_from({
    'tags': ['Projeções'],
    'summary': 'Gerar projeções de gastos',
    'description': 'Gera uma projeção de gastos futuros para um usuário específico com base em seu histórico de movimentações.',
    'parameters': [
        {
            'name': 'usuario',
            'in': 'query',
            'required': True,
            'type': 'integer',
            'description': 'ID do usuário para o qual as projeções serão geradas'
        }
    ],
    'responses': {
        200: {
            'description': 'Projeções de gastos geradas com sucesso',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'mes': {
                            'type': 'string',
                            'description': 'Mês da projeção'
                        },
                        'valor_projetado': {
                            'type': 'number',
                            'format': 'float',
                            'description': 'Valor projetado para o mês'
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Usuário não autorizado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem de erro de autorização'
                    }
                }
            }
        }
    }
})
def projections():
    user = request.args.get('usuario')
    valido = user_authorization.get_autorizacao_usuario(user)
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401

    projections = services.generate_projections(user)
    return jsonify(projections),200

@auxiliar_bp.route('/graph', methods=['GET'])
@swag_from({
    'tags': ['Gráfico'],
    'summary': 'Obter dados para o gráfico de uma carteira',
    'description': 'Retorna os dados para geração de um gráfico baseado nas movimentações de uma carteira específica.',
    'parameters': [
        {
            'name': 'wallet',
            'in': 'query',
            'required': True,
            'type': 'integer',
            'description': 'ID da carteira para a qual os dados do gráfico serão gerados. Deve ser um valor inteiro válido.'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados do gráfico retornados com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'description': 'Lista com dados para geração do gráfico.',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'date': {
                                    'type': 'string',
                                    'format': 'date',
                                    'description': 'Data da movimentação associada.'
                                },
                                'value': {
                                    'type': 'number',
                                    'description': 'Valor da movimentação no respectivo dia.'
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'O parâmetro "wallet" não é um número inteiro válido.',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': "O parâmetro 'wallet' deve ser um valor inteiro."
                    }
                }
            }
        },
        404: {
            'description': 'Parâmetro "wallet" ausente ou carteira não encontrada.',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': "O parâmetro 'wallet' é obrigatório."
                    }
                }
            }
        }
    }
})
def graph():
    wallet = request.args.get('wallet')
    if not wallet:
        return jsonify({"error": "O parâmetro 'wallet' é obrigatório."}), 404
    
    try:
        wallet = int(wallet)
    except ValueError:
        return jsonify({"error": "O parâmetro 'wallet' deve ser um valor inteiro."}), 400
    
    data = services.get_data_graph(wallet)
    return jsonify(data),200
