from app.extensions import mongo
from app.core.ports import BillRepository
from app.core.models import Bill
from pymongo import DESCENDING

class MongoBillRepository(BillRepository):
    def add(self, bill):
        mongo.db.bills.insert_one(bill.to_dict())

    def get_next_id(self):
        registro = mongo.db.bills.find().sort("bill", DESCENDING).limit(1)
        registro = list(registro)
        
        if registro:
            registro = registro[0]
        
        return registro["bill"] + 1 if registro else 1

    def find_by_user_id(self, user_id):
        bills_data = mongo.db.bills.find({'user_id': user_id})
        return [Bill.from_dict(bill) for bill in bills_data]
    
    def update(self, bill, description, category, valor, usuario):
        bill_data = mongo.db.bills.find({"bill": bill, "usuario": usuario})
        registro = list(bill_data)
        if not registro:
            return False
        if registro[0]['type'] == 2:
            valor_parcela = float(valor/registro[0]["parcela"])
            valor_parcela = round(valor_parcela,2)

        result = mongo.db.bills.update_one(
            {"bill": bill},
            {"$set": {"description": description, "category":category, "valor_compra":valor, "valor_parcela": valor_parcela}}
        )

        return result if result else None

    def existe_conta(self, id, usuario):
        bill_data = mongo.db.bills.find({"bill": id, "usuario": usuario})
        registro = list(bill_data)
        return True if registro else False
    
    def delete(self, bill):
        result = mongo.db.bills.delete_one({"bill": bill})
        if result.deleted_count > 0:
            return result
        else:
            return None

    def get_all_by_user_id(self, id):
        bill_data = mongo.db.bills.find({'usuario': id})
        return bill_data if bill_data else None
    
    def get_bill_by_id(self, id):
        bill_data = mongo.db.bills.find_one({"bill": id})
        return bill_data if bill_data else None
    
    def pagar_parcela(self, id):
        bill_data = mongo.db.bills.find({"bill": id})
        registro = list(bill_data)
        if not registro:
            return False
        
        parcela = int(registro[0]['parcela_paga']) + 1

        result = mongo.db.bills.update_one(
            {"bill": id},
            {"$set": {"parcela_paga": parcela}}
        )

        return result if result else None


        return super().pagar_parcela(id)