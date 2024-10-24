from flasgger import Swagger
from app import create_app

app = create_app()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',  
            "rule_filter": lambda rule: True,  
            "model_filter": lambda tag: True,  
        }
    ],
    "static_url_path": "/flasgger_static", 
    "swagger_ui": True,
    "specs_route": "/app1/apidocs/"
}


swagger = Swagger(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
