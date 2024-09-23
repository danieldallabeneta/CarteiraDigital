from flask import Blueprint
from .routes import movement_bp
from app.core.service import MovementService
from .adapters import MongoMovementRepository

movement_service = MovementService(MongoMovementRepository())

def init_movement(app):
    app.register_blueprint(movement_bp, url_prefix='/movement')