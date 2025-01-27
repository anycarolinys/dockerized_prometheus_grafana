from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Summary, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Métricas para o Prometheus

# Conta o número total de requisições HTTP recebidas
REQUEST_TOTAL_COUNTER = Counter(
    'http_requests_total',
    'Total de requisições HTTP recebidas',
    ['method', 'status_code']
)

# Registra a duração das requisições e as distribui em intervalos 
# Neste caso os intervalos vão de 10 a 100 segundos
REQUEST_DURATION_HISTOGRAM = Histogram(
    'http_request_duration_seconds',
    'Duração das requisições HTTP em segundos',
    buckets=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
)

# Registra quantis configuráveis de duração de requisições, como percentis 
# Fornece soma e contagem das durações
REQUEST_DURATION_SUMMARY = Summary(
    'http_request_duration_summary_seconds',
    'Resumo da duração das requisições HTTP em segundos',
    ['method']
)

# Função auxiliar para simular atraso
# Simula um delay em segundos
def sleep(ms):
    time.sleep(ms / 1000)

# Rota principal para processar requisições
@app.route('/')
def index():
    # Lê o parâmetro "success" da URL para determinar o código de status
    success = request.args.get('success', 'true').lower() == 'true'
    status_code = 200 if success else 500
    
    # Incrementa o contador total de requisições com os rótulos correspondentes
    REQUEST_TOTAL_COUNTER.labels(method='GET', status_code=str(status_code)).inc()
    
    # Mede o tempo de processamento da requisição
    start_time = time.time()
    sleep(100 * random.random())  
    duration_time = (time.time() - start_time) * 1000
    
    # Captura a duração das requisições
    REQUEST_DURATION_HISTOGRAM.observe(duration_time)
    REQUEST_DURATION_SUMMARY.labels(method='GET').observe(duration_time)

    return jsonify({
        'success': success,
        'data': {'message': f'Requisição realizada em {duration_time:.2f} ms.'}
    }), status_code

# Rota para obter as métricas do Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Ponto de partida da aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)