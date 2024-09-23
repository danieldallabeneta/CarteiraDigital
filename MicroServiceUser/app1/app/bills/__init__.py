from flask import Blueprint
from .routes import bills_bp
from .adapters import MongoBillRepository
from app.core.service import BillService

# Inicializar o serviço e conectar ao adaptador específico
bill_service = BillService(MongoBillRepository())

# Registrar o Blueprint
def init_bills(app):
    app.register_blueprint(bills_bp, url_prefix='/bills')
