from .config import Config
from .routes import auxiliar_bp

def create_app(app):

    app.config.from_object(Config)

    app.register_blueprint(auxiliar_bp, url_prefix='/aux')    
