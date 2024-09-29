from abc import ABC, abstractmethod

class WalletRepository(ABC):
    @abstractmethod
    def add(self, wallet):
        pass

    @abstractmethod
    def delete(self, wallet):
        pass

    @abstractmethod
    def get_by_user_id(self, user_id):
        pass

    @abstractmethod
    def get_by_user_and_wallet(self, usuario, wallet):
        pass

    @abstractmethod
    def get_next_id_by_user(self):
        pass

    @abstractmethod
    def get_all_by_user_id(self, user_id):
        pass

    @abstractmethod
    def add_found(self, wallet, valor):
        pass

    @abstractmethod
    def remove_found(self, wallet, valor):
        pass

class CategoryRepository(ABC):
    @abstractmethod
    def add(self, category):
        pass

    @abstractmethod
    def delete(self, category):
        pass

    @abstractmethod
    def update_category(self, category, new_name):
        pass

    @abstractmethod
    def get_next_id(self):
        pass

    @abstractmethod
    def get_all_by_user_id(self, usuario):
        pass

    @abstractmethod
    def existe_categoria(self, id, usuario):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

class BillRepository(ABC):
    @abstractmethod
    def add(self, bill):
        pass

    @abstractmethod
    def get_next_id(self):
        pass

    @abstractmethod
    def update(self,bill, description, category, valor, usuario):
        pass

    @abstractmethod
    def delete(self, bill):
        pass

    @abstractmethod
    def existe_conta(self, id, usuario):
        pass

    @abstractmethod
    def get_all_by_user_id(self, id):
        pass

    @abstractmethod
    def get_bill_by_id(self, id):
        pass

    @abstractmethod
    def pagar_parcela(self, id):
        pass

class MovementRepository(ABC):
    @abstractmethod
    def add(self, movement):
        pass

    @abstractmethod
    def get_all_by_user(self, usuario):
        pass