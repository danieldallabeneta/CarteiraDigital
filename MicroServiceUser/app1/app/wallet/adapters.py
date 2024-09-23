from app.extensions import mongo
from app.core.ports import WalletRepository
from app.core.models import Wallet
from pymongo import DESCENDING

class MongoWalletRepository(WalletRepository):
    def add(self, wallet):
        return mongo.db.wallets.insert_one(wallet.to_dict())

    def get_by_user_id(self, user_id):
        wallet_data = mongo.db.wallets.find_one({'wallet': user_id})
        return wallet_data if wallet_data else None
    
    def get_by_user_and_wallet(self, usuario, wallet):
        wallet_data = mongo.db.wallets.find_one({'usuario': usuario,'wallet':wallet})
        return Wallet.from_dict(wallet_data) if wallet_data else None
    
    def get_next_id_by_user(self):
        registro = mongo.db.wallets.find()
        if registro is None:
           return 1
        registro = mongo.db.wallets.find().sort("wallet", DESCENDING).limit(1)
        registro = list(registro)
        
        if registro:
            registro = registro[0]
        
        return registro["wallet"] + 1 if registro else 1

    def get_all_by_user_id(self, usuario):
        wallet_data = mongo.db.wallets.find({'usuario': usuario})
        return wallet_data if wallet_data else None

    def add_found(self, wallet, valor):
        wallet_data = mongo.db.wallets.find_one({"wallet": wallet})
        
        if not wallet_data:
            raise ValueError("Carteira não encontrada para o id especificado.")

        saldo_atual = float(wallet_data['saldo'])  
        valor_adicao = round(saldo_atual + float(valor),2)
        
        result = mongo.db.wallets.update_one(
            {"wallet": wallet},
            {"$set": {"saldo": valor_adicao}}
        )

        return result if result else None
    
    def remove_found(self, wallet, valor):
        wallet_data = mongo.db.wallets.find_one({'wallet': wallet})
        
        if not wallet_data:
            raise ValueError("Carteira não encontrada para o id especificado.")

        saldo_atual = float(wallet_data['saldo'])  
        valor_adicao = round(saldo_atual - float(valor),2)
                
        result = mongo.db.wallets.update_one(
            {"wallet": wallet},
            {"$set": {"saldo": valor_adicao}}
        )

        return result if result else None
    
    def delete(self, wallet):
        id_wallet = int(wallet)
        wallet_data = mongo.db.wallets.find({"wallet": id_wallet})
        registro = list(wallet_data)
        if registro:
            result = mongo.db.wallets.delete_one({"_id": registro[0]['_id']})
            return result if result else None
        else:
           return None