from flask import Blueprint, jsonify, request
from .services import generate_projections

api = Blueprint('api', __name__)

@api.route('/projections', methods=['POST'])
def projections():
    user = request.json.get('user')
    projections = generate_projections(user)
    return jsonify(projections)
