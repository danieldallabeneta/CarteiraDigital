import requests

class UserAuthorization():

    def get_autorizacao_usuario(self, id):
        url = "http://api-gateway/app2/aut/"+str(id)    
        response = requests.get(url)
        if response.status_code == 401:
            return False
        return True