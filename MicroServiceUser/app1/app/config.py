import os

class Config:

    MONGO_URI = "mongodb://mongo:27017/wallet_user"

    SWAGGER_ENABLED = os.getenv("SWAGGER_ENABLED", "false").lower() == "true"
