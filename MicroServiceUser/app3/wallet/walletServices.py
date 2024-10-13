import requests

class WalletServices():

    def get_dados_historico_user(self, user):       
        url = "http://api-gateway/app1/movement/get_all?usuario="+user
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Dados não encontrados"}, 404
        
    def get_dados_historico_wallet(self, wallet):       
        url = "http://api-gateway/app1/movement/get?wallet="+wallet
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Dados não encontrados"}, 404