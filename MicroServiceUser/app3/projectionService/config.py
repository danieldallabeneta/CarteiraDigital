import os

class Config:

    SWAGGER_ENABLED = os.getenv("SWAGGER_ENABLED", "false").lower() == "true"