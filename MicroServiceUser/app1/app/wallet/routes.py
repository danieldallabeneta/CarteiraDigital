import os
from flask import Blueprint, jsonify, request
from flasgger import swag_from

from .adapters import MongoWalletRepository
from app.movement.adapters import MongoMovementRepository
from app.bills.adapters import MongoBillRepository
from app.core.service import WalletService, MovementService, BillService
from datetime import datetime
from app.authorization.userAuthorization import UserAuthorization

wallet_bp = Blueprint('wallet', __name__)
wallet_service = WalletService(MongoWalletRepository())
movement_service = MovementService(MongoMovementRepository())
bill_service = BillService(MongoBillRepository())
user_authorization = UserAuthorization()

@wallet_bp.route('/add_wallet', methods=['POST'])
@swag_from({
    'tags': ['Carteira'],
    'summary': 'Adicionar uma nova carteira',
    'description': 'Cria uma nova carteira com os dados fornecidos.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Data de criação da carteira'
                    },
                    'nome': {
                        'type': 'string',
                        'description': 'Nome da carteira'
                    },
                    'saldo': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Saldo inicial da carteira'
                    },
                    'usuario': {
                        'type': 'integer',
                        'description': 'ID do usuário que está criando a carteira'
                    }
                },
                'required': ['data', 'nome', 'saldo', 'usuario']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Carteira criada com sucesso',
            'schema': {
                'type': 'boolean'
            }
        },
        400: {
            'description': 'Erro de solicitação, campos obrigatórios não fornecidos',
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
def add_wallet():
    data = request.json
    
    required_fields = ["data", "nome", "saldo", "usuario"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Todos os campos (data, nome, usuario, saldo) são obrigatórios"}), 400
    
    valido = user_authorization.get_autorizacao_usuario(data["usuario"])
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401

    wallet = wallet_service.create_wallet(data)
    wallet_data = wallet.to_dict()
    wallet_id = wallet_data["wallet"]
    movement_data = {
        "type":1,
        "wallet":wallet_id,
        "bill": None,
        "parcela": None,
        "date": datetime.now(),
        "value":wallet_data["saldo"],
        "usuario": wallet_data["usuario"],
        "info": f"Criação da carteira {wallet_id}"
    }

    movement_service.create_movement(movement_data)

    return jsonify(True) if wallet else jsonify(False), 201

@wallet_bp.route('/get_all', methods=['GET'])
@swag_from({
    'tags': ['Carteira'],
    'summary': 'Obter todas as carteiras de um usuário',
    'description': 'Retorna todas as carteiras associadas ao usuário fornecido.',
    'parameters': [
        {
            'name': 'usuario',
            'in': 'query',
            'required': True,
            'type': 'integer',
            'description': 'ID do usuário cujas carteiras devem ser retornadas'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de carteiras do usuário',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'wallet': {
                            'type': 'string',
                            'description': 'ID da carteira'
                        },
                        'date': {
                            'type': 'string',
                            'format': 'date',
                            'description': 'Data de criação da carteira'
                        },
                        'nome': {
                            'type': 'string',
                            'description': 'Nome da carteira'
                        },
                        'saldo': {
                            'type': 'number',
                            'format': 'float',
                            'description': 'Saldo da carteira'
                        },
                        'usuario': {
                            'type': 'integer',
                            'description': 'ID do usuário associado à carteira'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Erro de solicitação, parâmetro de usuário não fornecido',
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
                        'description': 'Mensagem de aviso'
                    }
                }
            }
        }
    }
})
def get_all_wallet():
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
    
    valido = user_authorization.get_autorizacao_usuario(usuario)
    if not valido:
        return jsonify({"error": "Usuário não autorizado"}), 401
    
    results = wallet_service.get_all_for_user(usuario)
    
    results_list = [{'wallet': doc['wallet'],'date': doc['data'].strftime("%d/%m/%Y"), 'nome': doc['nome'], 'saldo': doc['saldo'], 'usuario': doc['usuario']} for doc in results]
    
    if results_list:
        return jsonify(results_list), 200
    else:
        return jsonify({'message': 'Nenhum registro encontrado para o usuário fornecido'}), 404

@wallet_bp.route('/add_found', methods=['PUT'])
@swag_from({
    'tags': ['Carteira'],
    'summary': 'Adicionar valor à carteira',
    'description': 'Adiciona um valor ao saldo de uma carteira existente.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'ID da carteira'
                    },
                    'valor': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Valor a ser adicionado à carteira'
                    }
                },
                'required': ['id', 'valor']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Saldo atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Mensagem de confirmação'
                    }
                }
            }
        },
        400: {
            'description': 'Erro de solicitação, campos obrigatórios não fornecidos',
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
            'description': 'Carteira não encontrada',
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
def add_found():
    data = request.json
    wallet = data.get('id')
    valor_adicao = data.get('valor')
    
    if valor_adicao is None or wallet is None:
        return jsonify({'error': 'Os campos de valor e carteira são obrigatórios'}), 400

    try:
        valor_adicao = float(valor_adicao)
    except ValueError:
        return jsonify({'error': 'O valor deve ser um número'}), 400

    wallet_register = wallet_service.get_wallet_by_id(wallet)

    if wallet_register:
        valido = user_authorization.get_autorizacao_usuario(wallet_register['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado"}), 401

    wallet_data = wallet_service.add_found(wallet,valor_adicao)

    if wallet_data.matched_count > 0:
        if wallet_data.modified_count > 0:
            carteira = wallet_service.get_wallet_by_id(wallet)
            movement_data = {
                "type":1,
                "wallet":wallet,
                "bill": None,
                "parcela": None,
                "date": datetime.now(),
                "value":valor_adicao,
                "usuario": carteira["usuario"],
                "info": f"Adicionado valor {valor_adicao} na carteira {wallet}"
            }

            movement_service.create_movement(movement_data)
            return jsonify({'message': 'Saldo atualizado com sucesso'}), 200
        else:
            return jsonify({'message': 'Nenhuma alteração foi feita no saldo'}), 200
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
@wallet_bp.route('/remove_found', methods=['PUT'])
@swag_from({
    'tags': ['Carteira'],
    'summary': 'Remover valor da carteira',
    'description': 'Remove um valor do saldo de uma carteira existente.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'ID da carteira'
                    },
                    'valor': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Valor a ser removido da carteira'
                    }
                },
                'required': ['id', 'valor']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Saldo atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Mensagem de confirmação'
                    }
                }
            }
        },
        400: {
            'description': 'Erro de solicitação, campos obrigatórios não fornecidos',
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
                        'description': 'Mensagem de erro'
                    }
                }
            }
        },
        404: {
            'description': 'Carteira não encontrada',
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
def remove_found():
    data = request.json
    wallet = data.get('id')
    valor_adicao = data.get('valor')
    
    # Validar os dados
    if valor_adicao is None or wallet is None:
        return jsonify({'error': 'Os campos de valor e carteira são obrigatórios'}), 400

    try:
        valor_adicao = float(valor_adicao)
    except ValueError:
        return jsonify({'error': 'Usuário deve ser um inteiro e valor deve ser um número'}), 400

    wallet_register = wallet_service.get_wallet_by_id(wallet)

    if wallet_register:
        valido = user_authorization.get_autorizacao_usuario(wallet_register['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado"}), 401

    wallet_data = wallet_service.remove_found(wallet,valor_adicao)

    if wallet_data.matched_count > 0:
        if wallet_data.modified_count > 0:
            carteira = wallet_service.get_wallet_by_id(wallet)
            movement_data = {
                "type":2,
                "wallet":wallet,
                "bill": None,
                "parcela": None,
                "date": datetime.now(),
                "value": -valor_adicao,
                "usuario": carteira["usuario"],
                "info": f"Removido valor {valor_adicao} na carteira {wallet}"
            }

            movement_service.create_movement(movement_data)
            return jsonify({'message': 'Saldo atualizado com sucesso'}), 200
        else:
            return jsonify({'message': 'Nenhuma alteração foi feita no saldo'}), 200
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404

@wallet_bp.route('/delete/<string:wallet>', methods=['DELETE'])
@swag_from({
    'tags': ['Carteira'],
    'summary': 'Excluir uma carteira',
    'description': 'Remove uma carteira do sistema.',
    'parameters': [
        {
            'name': 'wallet',
            'in': 'path',
            'required': True,
            'type': 'string',
            'description': 'ID da carteira a ser excluída'
        }
    ],
    'responses': {
        200: {
            'description': 'Carteira excluída com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Mensagem de confirmação'
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
                        'description': 'Mensagem de erro'
                    }
                }
            }
        },
        404: {
            'description': 'Carteira não encontrada',
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
def delete_wallet(wallet):

    wallet_register = wallet_service.get_wallet_by_id(wallet)

    if wallet_register:
        valido = user_authorization.get_autorizacao_usuario(wallet_register['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado"}), 401

    result = wallet_service.delete(wallet)
    
    if not result:
        return jsonify({'error': 'Carteira não encontrada'}), 404

    if result.deleted_count > 0:
        return jsonify({'message': 'Carteira excluída com sucesso'}), 200
    else:
        return jsonify({'error': 'Carteira não encontrada'}), 404

@wallet_bp.route('/payment', methods=['PUT'])
@swag_from({
    'tags': ['Carteira'],
    'summary': 'Realizar pagamento de uma conta',
    'description': 'Realiza o pagamento de uma conta utilizando o saldo de uma carteira.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'wallet': {
                        'type': 'string',
                        'description': 'ID da carteira a ser usada para o pagamento'
                    },
                    'bill': {
                        'type': 'string',
                        'description': 'ID da conta a ser paga'
                    },
                    'usuario': {
                        'type': 'integer',
                        'description': 'ID do usuário que está realizando o pagamento'
                    }
                },
                'required': ['wallet', 'bill', 'usuario']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Pagamento realizado com sucesso',
            'schema': {
                'type': 'boolean'
            }
        },
        400: {
            'description': 'Erro de solicitação, condições de pagamento não atendidas',
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
                        'description': 'Mensagem de erro'
                    }
                }
            }
        },
        404: {
            'description': 'Carteira ou conta não encontrada',
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
def payment():
    data = request.json
    wallet_data  = data.get('wallet')
    bill_data    = data.get('bill')
    usuario_data = data.get('usuario')

    wallet_register = wallet_service.get_wallet_by_id(usuario_data)

    if wallet_register:
        valido = user_authorization.get_autorizacao_usuario(wallet_register['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado"}), 401

    carteira = wallet_service.get_wallet_by_id(wallet_data)
    if carteira:
        if carteira["usuario"] != usuario_data:
            return jsonify({'error': 'A carteira informada não pertence ao usuário.'}), 400
    else:
        return jsonify({'error': 'Carteira não encontrada.'}), 404
    
    conta = bill_service.get_bill_by_id(bill_data)
    if conta:
        if conta['usuario'] != usuario_data:
            return jsonify({'error': 'A conta informada não pertence ao usuário.'}), 400
    else:
        return jsonify({'error': 'Conta não encontrada.'}), 404

    if conta['parcela'] == conta['parcela_paga']:
        return jsonify({'error': 'A conta já está paga.'}), 400

    b_conta_parcelada = conta['type'] == 2
    saldo_carteira = round(float(carteira['saldo']),2)
    valor_conta = round(float(conta['valor_parcela']),2) if b_conta_parcelada else round(float(conta['valor_compra']),2)

    if saldo_carteira < valor_conta:
        return jsonify({'error': 'O saldo da carteira é menor que o valor a ser pago da conta.'}), 400
    
    #diminui saldo da carteira
    wallet_service.remove_found(wallet_data, valor_conta)
    
    parcela_paga = int(conta['parcela_paga']) + 1
    movement_data = {
        "type":2,
        "wallet":wallet_data,
        "bill": bill_data,
        "parcela": parcela_paga,
        "date": datetime.now(),
        "value": valor_conta,
        "usuario": usuario_data,
        "info": f"Pagamento da conta {conta['description']}, parcela {parcela_paga}, valor R${valor_conta}"
    }
    #cria a movimentação de saída da carteira
    movement_service.create_movement(movement_data)
    #atualiza a conta para reduzir a parcela a ser paga
    bill_service.pagar_parcela(bill_data)

    return jsonify(True),200

@wallet_bp.route('/transfer', methods=['PUT'])
@swag_from({
    'tags': ['Carteira'],
    'summary': 'Transferir valor entre carteiras',
    'description': 'Transfere um valor de uma carteira para outra.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'origem': {
                        'type': 'string',
                        'description': 'ID da carteira de origem'
                    },
                    'destino': {
                        'type': 'string',
                        'description': 'ID da carteira de destino'
                    },
                    'valor': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Valor a ser transferido'
                    }
                },
                'required': ['origem', 'destino', 'valor']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Transferência realizada com sucesso',
            'schema': {
                'type': 'boolean'
            }
        },
        400: {
            'description': 'Erro de solicitação, condições de transferência não atendidas',
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
            'description': 'Usuário não autorizado ou saldo insuficiente',
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
        404: {
            'description': 'Carteira de destino não encontrada',
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
def transfer():
    data = request.json
    origem = data.get('origem')
    destino = data.get('destino')

    wallet_origem = wallet_service.get_wallet_by_id(origem)    
    wallet_destino = wallet_service.get_wallet_by_id(destino)

    if wallet_origem:
        valido = user_authorization.get_autorizacao_usuario(wallet_origem['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado"}), 401
        
    if wallet_destino:
        valido = wallet_origem['usuario'] == wallet_destino['usuario']
        if not valido:
            return jsonify({"error": "Carteira de destino não pertence ao usuário da carteira de origem"}), 401
    else:
        return jsonify({'error': 'Carteira de destino não encontrada.'}), 404

    valor = data.get('valor')

    if float(wallet_origem['saldo']) < float(valor):
        return jsonify({"error": "Saldo insuficiente."}), 401
    
    wallet_service.remove_found(origem,valor)
    movement_data = {
        "type":2,
        "wallet":origem,
        "bill": None,
        "parcela": None,
        "date": datetime.now(),
        "value": valor,
        "usuario": wallet_origem['usuario'],
        "info": f"Transferência do valor R$ {valor} para a carteira código {destino} - {wallet_destino['nome']}"
    }
    #cria a movimentação de saída da carteira
    movement_service.create_movement(movement_data)

    wallet_service.add_found(destino,valor)

    movement_data = {
        "type":1,
        "wallet":destino,
        "bill": None,
        "parcela": None,
        "date": datetime.now(),
        "value": valor,
        "usuario": wallet_origem['usuario'],
        "info": f"Recebido o valor R$ {valor} da carteira código {origem} - {wallet_origem['nome']}"
    }
    #cria a movimentação de saída da carteira
    movement_service.create_movement(movement_data)
    return jsonify(True),200

@wallet_bp.route('/balace', methods=['GET'])
@swag_from({
    'tags': ['Carteira'],
    'summary': 'Obter saldo da carteira',
    'description': 'Retorna o saldo atual de uma carteira.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'wallet': {
                        'type': 'string',
                        'description': 'ID da carteira para a qual se deseja obter o saldo'
                    }
                },
                'required': ['wallet']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Saldo da carteira obtido com sucesso',
            'schema': {
                'type': 'number',
                'format': 'float',
                'description': 'Saldo da carteira'
            }
        },
        401: {
            'description': 'Usuário não autorizado',
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
        404: {
            'description': 'Carteira não encontrada',
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
def balance():
    data = request.json
    wallet = data.get('wallet')

    wallet_origem = wallet_service.get_wallet_by_id(wallet) 

    if wallet_origem:
        valido = user_authorization.get_autorizacao_usuario(wallet_origem['usuario'])
        if not valido:
            return jsonify({"error": "Usuário não autorizado"}), 401
    else:
         return jsonify({'error': 'Carteira não encontrada.'}), 404
    
    return jsonify(wallet_origem['saldo']),200
