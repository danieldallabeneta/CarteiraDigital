from app.extensions import mongo
from app.core.ports import MovementRepository
from app.core.models import Movement

class MongoMovementRepository(MovementRepository):
    def add(self, movement):
        mongo.db.movement.insert_one(movement.to_dict())
    
    def get_all_by_user(self, usuario):
        movement_data = mongo.db.movement.find({'usuario': usuario})
        return movement_data if movement_data else None