from flask_pymongo import PyMongo

mongo = PyMongo()

def init_extensions(app):
    mongo.init_app(app)
    db = mongo.db

    if "wallets" not in db.list_collection_names():
        db.create_collection("wallets")
        
    if "bills" not in db.list_collection_names():
        db.create_collection("bills")
    
    if "category" not in db.list_collection_names():
        db.create_collection("category")
    
    if "movement" not in db.list_collection_names():
        db.create_collection("movement")
        
