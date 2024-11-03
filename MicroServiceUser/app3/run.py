from flask import Flask
from flasgger import Swagger
from prometheus_client import make_wsgi_app, Counter, Histogram, Summary, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from projectionService import create_app

app = Flask(__name__)
create_app(app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests')
REQUEST_LATENCY = Summary('request_latency_seconds', 'Latency of HTTP requests')
REQUEST_SIZE = Histogram('request_size_bytes', 'Size of HTTP requests')
ACTIVE_REQUESTS = Gauge('active_requests', 'Number of active requests')

swagger = Swagger(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
