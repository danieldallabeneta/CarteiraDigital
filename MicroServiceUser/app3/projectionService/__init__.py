from .routes import auxiliar_bp

def create_app(app):
    app.register_blueprint(auxiliar_bp, url_prefix='/aux')    
