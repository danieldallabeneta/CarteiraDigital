class Wallet:
    def __init__(self, wallet, data, nome,  usuario, saldo=0):
        self.wallet = wallet
        self.data = data
        self.nome = nome
        self.saldo = saldo
        self.usuario = usuario

    def to_dict(self):
        return {
            "wallet": self.wallet,
            "data": self.data,
            "nome": self.nome,
            "saldo": self.saldo,
            "usuario": self.usuario
        }
    
    @staticmethod
    def from_dict(data):
        return Wallet(wallet=data.get('wallet'), data=data.get('data'),nome=data.get('nome'),saldo=data.get('saldo'),usuario=data.get('usuario'))
    
class Category:
    def __init__(self, category, name, usuario):
        self.category = category
        self.name = name
        self.usuario = usuario

    def to_dict(self):
        return {
            "category": self.category,
            "name": self.name,
            "usuario": self.usuario
        }
    
    @staticmethod
    def from_dict(data):
        return Category(category=data.get('category'), name=data.get('name'), usuario=data.get('usuario'))

class Bill:
    def __init__(self, bill, description, valor_compra, include_date, due_date, type, parcela, category, usuario, valor_parcela, parcela_paga):
        self.bill = bill
        self.description = description
        self.valor_compra = valor_compra
        self.include_date = include_date
        self.due_date = due_date
        self.type = type
        self.parcela = parcela
        self.category = category
        self.usuario = usuario
        self.valor_parcela = valor_parcela
        self.parcela_paga = parcela_paga

    def to_dict(self):
        return {
            'bill': self.bill,
            'description': self.description,
            'valor_compra': self.valor_compra,
            'include_date': self.include_date,
            'due_date': self.due_date,
            'type': self.type,
            'parcela': self.parcela,
            'category': self.category,
            'usuario': self.usuario,
            'valor_parcela': self.valor_parcela,
            'parcela_paga': self.parcela_paga
        }

    @staticmethod
    def from_dict(data):
        return Bill(
            bill=data.get('bill'),
            description=data.get('description'),
            valor_compra=data.get('valor_compra'),
            include_date=data.get('include_date'),            
            due_date=data.get('due_date'),
            type=data.get('type'),
            parcela=data.get('parcela'),
            category=data.get('category'),
            usuario=data.get('usuario'),
            valor_parcela=data.get('valor_parcela'),
            parcela_paga=data.get('parcela_paga')
        )
    
class Movement():
    def __init__(self, type, wallet, bill, parcela, date, value, usuario, info):
        self.type = type
        self.wallet = wallet
        self.bill = bill
        self.parcela = parcela
        self.date = date
        self.value = value
        self.usuario = usuario    
        self.info = info

    def to_dict(self):
        return {
            'type': self.type,
            'wallet': self.wallet,
            'bill': self.bill,
            'parcela': self.parcela,
            'date': self.date,
            'value': self.value,
            'usuario': self.usuario,
            'info': self.info
        }
    
    @staticmethod
    def from_dict(data):
        return Movement(
            type=data.get('type'),
            wallet=data.get('wallet'),
            bill=data.get('bill'),
            parcela=data.get('parcela'),
            date=data.get('date'),            
            value=data.get('value'),
            usuario=data.get('usuario'),
            info=data.get('info')
        )
