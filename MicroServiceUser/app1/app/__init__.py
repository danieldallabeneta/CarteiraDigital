from flask import Flask
from .config import Config
from .extensions import init_extensions
from .wallet import init_wallet  
from .bills import init_bills  
from .category import init_category  
from .movement import init_movement

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa as extensões
    init_extensions(app)

    # Inicializa os módulos com Blueprints
    init_wallet(app)
    init_bills(app)
    init_category(app)
    init_movement(app)

    return app
