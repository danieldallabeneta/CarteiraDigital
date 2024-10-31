from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from app import create_app

app = create_app()

metrics = PrometheusMetrics(app)
swagger = Swagger(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
