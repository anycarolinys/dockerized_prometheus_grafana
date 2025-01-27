# Demanda 5  

https://medium.com/xp-inc/monitorando-aplica%C3%A7%C3%B5es-docker-com-prometheus-e-grafana-593f507fc17

https://medium.com/@letathenasleep/exposing-python-metrics-with-prometheus-c5c837c21e4d

- metricas nao aparecem no prometheus 
- olhei o docker logs prometheus - nao indicava erro
- testei se as metricas estavam sendo retornadas com curl http://localhost:5000/metrics
- descobri que havia um erro com uma das metricas do app atraves do docker-compose logs
- o problema é que algumas métricas não estavam com as labels devidamente configuradas e é essencial
- Fui olhar a documentacao (nao achei em foruns) para entender o que era necessário nas labels  para cada tipo de métrica (Gauge, Summary, Counter)
    - https://prometheus.github.io/client_python/instrumenting/counter/
    - https://prometheus.github.io/client_python/instrumenting/labels/
