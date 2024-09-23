from flask import Blueprint
from .routes import category_bp
from .adapters import MongoCategoryRepository
from app.core.service import CategoryService

# Inicializar o serviço e conectar ao adaptador específico
category_service = CategoryService(MongoCategoryRepository())

# Registrar o Blueprint
def init_category(app):
    app.register_blueprint(category_bp, url_prefix='/category')