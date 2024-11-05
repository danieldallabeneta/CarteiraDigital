import requests

class UserAuthorization():

    def get_autorizacao_usuario(self, id):
        url = "http://host.docker.internal:8080/aut/"+str(id)    
        response = requests.get(url)
        if response.status_code == 401:
            return False
        return True