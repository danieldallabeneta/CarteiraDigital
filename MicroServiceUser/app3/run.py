from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from projectionService import create_app

app = create_app()

swagger = Swagger(app)
metrics = PrometheusMetrics(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
