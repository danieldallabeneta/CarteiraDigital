import os
from flask import Blueprint, jsonify, request
from flasgger import swag_from

from .adapters import MongoBillRepository
from app.category.adapters import MongoCategoryRepository
from app.core.service import BillService, CategoryService
from datetime import datetime
from app.authorization.userAuthorization import UserAuthorization

bills_bp = Blueprint('bills', __name__)
bill_service = BillService(MongoBillRepository())
category_service = CategoryService(MongoCategoryRepository())
user_authorization = UserAuthorization()

@bills_bp.route('/add', methods=['POST'])
@swag_from({
    'tags': ['Contas'],
    'summary': 'Adicionar uma nova conta',
    'description': 'Este endpoint permite adicionar uma nova conta, incluindo detalhes como descrição, valor, data de inclusão, data de vencimento, tipo de conta e usuário associado.',
    'parameters': [
        {
            'name': 'body',
            'description': 'Dados da conta a ser adicionada',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'description': {
                        'type': 'string',
                        'description': 'Descrição da conta',
                        'required': True
                    },
                    'valor_compra': {
                        'type': 'number',
                        'description': 'Valor da conta',
                        'required': True
                    },
                    'include_date': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Data de inclusão da conta',
                        'required': True
                    },
                    'due_date': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Data de vencimento da conta',
                        'required': True
                    },
                    'type': {
                        'type': 'integer',
                        'description': 'Tipo da conta (1: à vista, 2: parcelada)',
                        'required': True
                    },
                    'usuario': {
                        'type': 'string',
                        'description': 'Usuário associado à conta',
                        'required': True
                    },
                    'parcela': {
                        'type': 'integer',
                        'description': 'Quantidade de parcelas (opcional para contas parceladas)'
                    },
                    'category': {
                        'type': 'string',
                        'description': 'Categoria da conta (opcional)'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Conta adicionada com sucesso',
            'schema': {
                'type': 'boolean'
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
        }
    }
})
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

    valido = user_authorization.get_autorizacao_usuario(usuario)
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401

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
@swag_from({
    'tags': ['Contas'],
    'summary': 'Atualizar uma conta existente',
    'description': 'Este endpoint permite atualizar os detalhes de uma conta existente com base no ID fornecido. Os campos atualizáveis incluem descrição, valor, categoria e usuário.',
    'parameters': [
        {
            'name': 'body',
            'description': 'Dados da conta a ser atualizada',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'ID da conta',
                        'required': True
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Nova descrição da conta'
                    },
                    'valor_compra': {
                        'type': 'number',
                        'description': 'Novo valor da conta',
                        'required': True
                    },
                    'category': {
                        'type': 'string',
                        'description': 'Nova categoria da conta (opcional)'
                    },
                    'usuario': {
                        'type': 'string',
                        'description': 'Usuário associado à conta',
                        'required': True
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Conta atualizada com sucesso',
            'schema': {
                'type': 'boolean'
            }
        },
        400: {
            'description': 'Erro de solicitação, campos obrigatórios faltando ou inválidos',
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
        }
    }
})
def update_bill():
    data = request.json
    id = data.get('id')
    description = data.get('description')
    category = data.get('category')
    valor_compra = data.get('valor_compra')
    usuario = data.get('usuario')

    valido = user_authorization.get_autorizacao_usuario(usuario)
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401

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
@swag_from({
    'tags': ['Contas'],
    'summary': 'Excluir uma conta',
    'description': 'Este endpoint permite excluir uma conta existente com base no ID fornecido. É necessário o usuário associado para realizar a operação.',
    'parameters': [
        {
            'name': 'body',
            'description': 'Dados da conta a ser excluída',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'ID da conta a ser excluída',
                        'required': True
                    },
                    'usuario': {
                        'type': 'string',
                        'description': 'Usuário associado à conta',
                        'required': True
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Conta excluída com sucesso',
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
            'description': 'Conta não encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem de erro'
                    }
                }
            }
        }
    }
})
def delete_bill():
    data = request.json
    id   = data.get('id')
    usuario = data.get('usuario')

    valido = user_authorization.get_autorizacao_usuario(usuario)
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401

    if id is None:
        return jsonify({"error": "Informe uma conta válida."}), 400
    
    if usuario is None:
        return jsonify({"error": "Informe um usuário válido."}), 400

    b_existe_conta = bill_service.existe_conta(id, usuario)
    if not b_existe_conta:
        return jsonify({"error": "Conta não encontrada para o usuário."}), 404

    result = bill_service.delete(id)
    if not result:
        return jsonify({'error': 'Conta não encontrada'}), 404

    return jsonify({'message': 'Conta excluída com sucesso'}), 200

@bills_bp.route('/all', methods=['GET'])
@swag_from({
    'tags': ['Contas'],
    'summary': 'Recuperar todas as contas de um usuário',
    'description': 'Este endpoint permite recuperar todas as contas associadas a um usuário específico. É necessário fornecer o ID do usuário como parâmetro.',
    'parameters': [
        {
            'name': 'usuario',
            'description': 'ID do usuário cujas contas devem ser recuperadas',
            'in': 'query',
            'required': True,
            'type': 'string'
        }
    ],
    'responses': {
        200: {
            'description': 'Contas recuperadas com sucesso',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string',
                            'description': 'ID da conta'
                        },
                        'nome': {
                            'type': 'string',
                            'description': 'Descrição da conta'
                        },
                        'valor_compra': {
                            'type': 'number',
                            'description': 'Valor da conta'
                        },
                        'data_inclusao': {
                            'type': 'string',
                            'format': 'date',
                            'description': 'Data de inclusão da conta'
                        },
                        'vencimento': {
                            'type': 'string',
                            'format': 'date',
                            'description': 'Data de vencimento da conta'
                        },
                        'forma_pagamento': {
                            'type': 'string',
                            'description': 'Forma de pagamento da conta'
                        },
                        'parcelas': {
                            'type': 'integer',
                            'description': 'Quantidade de parcelas, se aplicável'
                        },
                        'usuario': {
                            'type': 'string',
                            'description': 'Usuário associado à conta'
                        },
                        'valor_parcela': {
                            'type': 'number',
                            'description': 'Valor da parcela'
                        },
                        'parcela_paga': {
                            'type': 'boolean',
                            'description': 'Indica se a parcela foi paga'
                        },
                        'categoria': {
                            'type': 'string',
                            'description': 'Categoria da conta'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Erro de solicitação, ID do usuário não fornecido',
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
        }
    }
})
def get_all_by_user():
    usuario = request.args.get('usuario')

    valido = user_authorization.get_autorizacao_usuario(usuario)
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401

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

