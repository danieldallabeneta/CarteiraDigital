from app.extensions import mongo
from app.core.ports import CategoryRepository
from app.core.models import Category
from pymongo import DESCENDING

class MongoCategoryRepository(CategoryRepository):
    def add(self, category):
        mongo.db.category.insert_one(category.to_dict())
    
    def delete(self, category):
        id_category = int(category)
        category_data = mongo.db.category.find({"category": id_category})
        registro = list(category_data)
        if registro:
            result = mongo.db.category.delete_one({"_id": registro[0]['_id']})
            return result if result else None
        else:
           return None

    def get_next_id(self):
        registro = mongo.db.category.find().sort("category", DESCENDING).limit(1)
        registro = list(registro)
        
        if registro:
            registro = registro[0]
        
        return registro["category"] + 1 if registro else 1

    def get_all_by_user_id(self, usuario):
        wallet_data = mongo.db.category.find({'usuario': usuario})
        return wallet_data if wallet_data else None
    
    def update_category(self,category, new_name):
        category_data = mongo.db.category.find({"category": category})
        if not category_data:
            raise ValueError("Categoria não encontrada.")
        
        result = mongo.db.category.update_one(
            {"category": category},
            {"$set": {"name": new_name}}
        )

        return result if result else None

    def existe_categoria(self, id, usuario):
        category_data = mongo.db.category.find({"category": id, "usuario": usuario})
        registro = list(category_data)
        return True if registro else False
    
    def find_by_id(self, id):
        category_data = mongo.db.category.find({"category": id})
        if not category_data:
            raise ValueError("Categoria não encontrada.")
        return category_data
