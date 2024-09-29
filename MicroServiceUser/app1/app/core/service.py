from app.core.ports import WalletRepository, BillRepository, CategoryRepository, MovementRepository
from app.core.models import Wallet, Bill, Category, Movement
from datetime import datetime

class WalletService:
    def __init__(self, repository: WalletRepository):
        self.repository = repository
    
    def create_wallet(self, wallet):
        data = datetime.strptime(wallet["data"], "%d/%m/%Y")
        nome = wallet["nome"]
        usuario = wallet["usuario"]
        saldo = round(float(wallet["saldo"]),2)
        id = self.repository.get_next_id_by_user()
        wallet = Wallet(id,data,nome,usuario,saldo)
        b_insert = self.repository.add(wallet)
        
        return wallet if b_insert else None
    
    def get_all_for_user(self, user_id):
        return self.repository.get_all_by_user_id(user_id)
    
    def add_found(self,wallet,valor):
        return self.repository.add_found(wallet,valor)
    
    def remove_found(self,wallet,valor):
        return self.repository.remove_found(wallet,valor)

    def delete(self, wallet):
        return self.repository.delete(wallet)  
    
    def get_wallet_by_id(self, id):
        return self.repository.get_by_user_id(id)    

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create_category(self, category):
        id = self.repository.get_next_id()
        name = category["name"]
        usuario = category["usuario"]        
        new_category = Category(id,name,usuario)
        self.repository.add(new_category)
        return new_category
    
    def delete(self, category):
        return self.repository.delete(category)  
    
    def get_all_for_user(self, usuario):
        return self.repository.get_all_by_user_id(usuario)
    
    def update_category(self, category, new_name):
        return self.repository.update_category(category,new_name)
    
    def existe_categoria(self,id,usuario):
        return self.repository.existe_categoria(id,usuario)
    
    def get_category_by_id(self, id):
        return self.repository.find_by_id(id)

class BillService:
    def __init__(self, repository: BillRepository):
        self.repository = repository

    def create_bill(self, bill):
        description   = bill['description']
        valor_compra  = bill['valor_compra']
        include_date  = datetime.strptime(bill['include_date'], "%d/%m/%Y")
        due_date      = datetime.strptime(bill['due_date'], "%d/%m/%Y")
        type          = bill['type']
        parcela       = bill['parcela']
        category      = bill['category']
        usuario       = bill['usuario']
        id            = self.repository.get_next_id()
        if type == 2:
            valor_parcela = float(valor_compra / parcela)
            valor_parcela = round(valor_parcela,2)
        parcela_paga  = 0

        bill = Bill(id,description,valor_compra,include_date,due_date,type,parcela,category,usuario,valor_parcela, parcela_paga)
        self.repository.add(bill)
        return bill

    def update_bill(self, bill, description, category, valor, usuario):
        return self.repository.update(bill, description, category, valor, usuario)

    def get_bills_for_user(self, user_id):
        return self.repository.find_by_user_id(user_id)
    
    def delete(self, bill):
        return self.repository.delete(bill)
    
    def existe_conta(self, id, usuario):
        return self.repository.existe_conta(id, usuario)
    
    def get_all_by_user_id(self, usuario):
        return self.repository.get_all_by_user_id(usuario)
    
    def get_bill_by_id(self, id):
        return self.repository.get_bill_by_id(id)
    
    def pagar_parcela(self, id):
        return self.repository.pagar_parcela(id)

class MovementService:
    def __init__(self, repository: MovementRepository):
        self.repository = repository

    def create_movement(self, movement):
        type = movement["type"]
        wallet = movement["wallet"]
        bill = movement["bill"]
        parcela = movement["parcela"]
        date = movement["date"]
        value = movement["value"]
        usuario = movement["usuario"]
        info = movement["info"]

        movement_data = Movement(type,wallet,bill,parcela,date,value,usuario,info)
        self.repository.add(movement_data)
        return movement_data
    
    def get_all_by_user_id(self, id):
        return self.repository.get_all_by_user(id)