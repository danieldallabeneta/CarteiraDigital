from flask import Blueprint, jsonify, request
from .adapters import MongoMovementRepository
from app.core.service import MovementService

movement_bp = Blueprint('movement', __name__)
movement_service = MovementService(MongoMovementRepository())