from flask import Blueprint
from .routes import wallet_bp
from .adapters import MongoWalletRepository
from app.core.service import WalletService

# Inicializar o serviço e conectar ao adaptador específico
wallet_service = WalletService(MongoWalletRepository())

# Registrar o Blueprint
def init_wallet(app):
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
