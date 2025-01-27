from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Summary, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

request_total_counter = Counter(
    'http_requests_total',
    'Total de requisições HTTP recebidas',
    ['method', 'status_code']
)

request_duration_histogram = Histogram(
    'http_request_duration_seconds',
    'Duração das requisições HTTP em segundos',
    buckets=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
)

request_duration_summary = Summary(
    'http_request_duration_summary_seconds',
    'Resumo da duração das requisições HTTP em segundos',
    ['method']
)

def sleep(ms):
    time.sleep(ms / 1000)

@app.route('/')
def index():
    success = request.args.get('success', 'true').lower() == 'true'
    status_code = 200 if success else 500
    
    request_total_counter.labels(method='GET', status_code=str(status_code)).inc()
    
    start_time = time.time()
    sleep(100 * random.random())  
    duration_time = (time.time() - start_time) * 1000
    
    
    request_duration_histogram.observe(duration_time)
    request_duration_summary.labels(method='GET').observe(duration_time)

    return jsonify({
        'success': success,
        'data': {'message': f'Requisição realizada em {duration_time:.2f} ms.'}
    }), status_code

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)