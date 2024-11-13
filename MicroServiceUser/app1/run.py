from flask import Flask
from flasgger import Swagger
from prometheus_client import make_wsgi_app, Counter, Histogram, Summary, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import create_app

app = Flask(__name__)
create_app(app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

REQUEST_COUNT_TOTAL = Counter('http_requests_total', 'Total number of HTTP requests')
REQUEST_LATENCY = Summary('request_latency_seconds', 'Latency of HTTP requests')
REQUEST_SIZE = Histogram('request_size_bytes', 'Size of HTTP requests')
ACTIVE_REQUESTS = Gauge('active_requests', 'Number of active requests')

REQUEST_COUNT= Counter('app_request_count','Application Request Count',['method', 'endpoint', 'http_status'])
REQUEST_LATENCY_HISTOGRAM = Histogram('app_request_latency_seconds','Application Request Latency', ['method', 'endpoint'])

if app.config['SWAGGER_ENABLED']:
    swagger = Swagger(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
