from urllib.parse import quote_plus

class Config:
    local = True    

    if local:
        MONGO_URI = "mongodb://mongo:27017/wallet_user"
        #MONGO_URI = "mongodb://localhost:27017/wallet_user"
    else:
        username = quote_plus('danieludesc')
        password = quote_plus('D@niel001')
        cluster_url = 'object.cyuri.mongodb.net'
        MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster_url}/wallet_user?retryWrites=true&w=majority"
