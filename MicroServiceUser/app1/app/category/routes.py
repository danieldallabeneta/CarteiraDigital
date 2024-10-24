import os
from flask import Blueprint, jsonify, request
from flasgger import swag_from

from .adapters import MongoCategoryRepository
from app.core.service import CategoryService
from app.authorization.userAuthorization import UserAuthorization

category_bp = Blueprint('category', __name__)
category_service = CategoryService(MongoCategoryRepository())
user_authorization = UserAuthorization()

yaml_path = os.path.join(os.path.dirname(__file__), 'category_documentation.yml')

@category_bp.route('/add', methods=['POST'])
@swag_from({
    'summary': 'Adicionar uma nova categoria',
    'description': 'Adiciona uma nova categoria no sistema para o usuário especificado.',
    'tags': ['Categoria'],
    'parameters': [
        {
            'name': 'body',
            'description': 'Dados da categoria a ser adicionada',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Nome da categoria',
                        'example': 'Alimentação'
                    },
                    'usuario': {
                        'type': 'string',
                        'description': 'Código Identificador do usuário',
                        'example': '12345'
                    }
                },
                'required': ['name', 'usuario']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Registro inserido com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Mensagem de sucesso'
                    }
                }
            }
        },
        400: {
            'description': 'Erro de solicitação, campos obrigatórios faltando',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem de erro informando campos obrigatórios'
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
        },
        404: {
            'description': 'Registro não inserido',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Mensagem informando que o registro não foi inserido'
                    }
                }
            }
        }
    }
}, validation=True)
def add_category():
    data = request.json
    
    required_fields = ["name", "usuario"]
    if not all(field in data for field in required_fields):
        return jsonify({"error":"Todos os campos (nome, usuario) são obrigatórios"}), 400

    valido = user_authorization.get_autorizacao_usuario(data['usuario'])
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401
        
    category = category_service.create_category(data)

    if category:
        return jsonify({"message": "Registro inserido com sucesso"}), 201 
    else:
        return jsonify({"message": "Registro não inserido"}), 404

@category_bp.route('/update_category', methods=['PUT'])
@swag_from({
    'summary': 'Atualizar uma categoria existente',
    'description': 'Atualiza o nome de uma categoria existente com base no ID fornecido.',
    'tags': ['Categoria'],
    'parameters': [
        {
            'name': 'body',
            'description': 'Dados da categoria a ser atualizada',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'ID da categoria a ser atualizada',
                        'example': '12345'
                    },
                    'name': {
                        'type': 'string',
                        'description': 'Novo nome da categoria',
                        'example': 'Educação'
                    }
                },
                'required': ['id', 'name']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Categoria atualizada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'sucesso': {
                        'type': 'string',
                        'description': 'Categoria Atualizada'
                    }
                }
            }
        },
        400: {
            'description': 'Erro de solicitação, campos obrigatórios faltando',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem de erro'
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
        },
        404: {
            'description': 'Categoria não atualizada',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem informando que a categoria não foi atualizada'
                    }
                }
            }
        }
    }
}, validation=True)
def update_category():
    data = request.json
    category= data.get('id')
    new_name = data.get('name')
    if category is None or new_name is None:
        return jsonify({'error': 'Os campos de id e name são obrigatórios.'}), 400

    category_register = category_service.get_category_by_id(category)
    if category_register:
        valido = user_authorization.get_autorizacao_usuario(category_register['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado."}), 401

    category_data = category_service.update_category(category,new_name)

    if category_data:
        return jsonify({"sucesso":"Categoria Atualizada."}), 201
    else:
        return jsonify({"error":"Categoria não atualizada."}), 404

@category_bp.route('/delete/<string:category>', methods=['DELETE'])
@swag_from({
    'summary': 'Excluir uma categoria',
    'description': 'Remove uma categoria do sistema com base no ID fornecido.',
    'tags': ['Categoria'],
    'parameters': [
        {
            'name': 'category',
            'in': 'path',
            'required': True,
            'type': 'string',
            'description': 'ID da categoria a ser excluída',
            'example': '12345'
        }
    ],
    'responses': {
        200: {
            'description': 'Categoria excluída com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'sucesso': {
                        'type': 'string',
                        'description': 'Mensagem de sucesso'
                    }
                }
            }
        },
        400: {
            'description': 'Erro de solicitação, categoria inválida',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem de erro'
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
        },
        404: {
            'description': 'Categoria não encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem informando que a categoria não foi encontrada'
                    }
                }
            }
        }
    }
}, validation=True)
def delete_category(category):
    category_register = category_service.get_category_by_id(category)
    if category_register:
        valido = user_authorization.get_autorizacao_usuario(category_register['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado."}), 401
        
    result = category_service.delete(category)
    
    if not result:
        return jsonify({"error": 'Carteira não encontrada.'}), 404

    if result.deleted_count > 0:
        return jsonify({"sucesso": "Carteira excluída com sucesso."}), 200
    else:
        return jsonify({"error": "Carteira não encontrada."}), 404

@category_bp.route('/get_all', methods=['GET'])
@swag_from({
    'summary': 'Todas as categoria',
    'description': 'Retorna todas as categoria do sistema com base no ID fornecido.',
    'tags': ['Categoria'],
    'parameters': [
        {
            'name': 'usuario',
            'description': 'ID do usuário para o qual as categorias devem ser retornadas',
            'type': 'integer',
            'required': True,
            'in': 'query'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de categorias para o usuário fornecido',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string',
                            'description': 'ID da categoria'
                        },
                        'nome': {
                            'type': 'string',
                            'description': 'Nome da categoria'
                        },
                        'usuario': {
                            'type': 'integer',
                            'description': 'ID do usuário ao qual a categoria pertence'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Erro de solicitação, parâmetros inválidos',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem de erro'
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
        },
        404: {
            'description': 'Nenhum registro encontrado para o usuário fornecido',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Mensagem informando que nenhum registro foi encontrado'
                    }
                }
            }
        }
    }
})
def get_all_category():
    usuario = request.args.get('usuario')
    
    if usuario is None:
        return jsonify({"error": "Parâmetro de usuário é obrigatório."}), 400
    
    try:
        usuario = int(usuario)
    except ValueError:
        return jsonify({"error": "O parâmetro de usuário deve ser um inteiro."}), 400
    
    valido = user_authorization.get_autorizacao_usuario(usuario)
    if not valido:
        return jsonify({"error": "Usuário não autorizado."}), 401
    
    results = category_service.get_all_for_user(usuario)
    
    results_list = [{'id': str(doc['category']), 'nome': doc['name'], 'usuario': doc['usuario']} for doc in results]
    
    if results_list:
        return jsonify(results_list), 200
    else:
        return jsonify({"message": "Nenhum registro encontrado para o usuário fornecido."}), 404





    




