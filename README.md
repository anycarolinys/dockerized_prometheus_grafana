# Demanda 5
Desenvolvida em ambiente WSL com Ubuntu 22.04.4 LTS e foi executada localmente utilizando o IP da máquina obtido com o comando ```ip a```.  

## **Como executar o projeto**  

1. Clone o repositório
```
git clone https://github.com/anycarolinys/dockerized_prometheus_grafana.git
```

2. Execute os containers em segundo plano 
```
docker-compose up --build -d 
```
Para execuções posteriores basta
```
docker-compose up -d 
```
3. Devem haver três containers em execução (Aplicação Flask, Prometheus, Grafana) confira com
```
docker ps
```

4. Para realizar requisições a API Flask
```
http://<localhost>:5000
```
Para solicitar uma requisição bem sucedida:  
```
http://<localhost>:5000/?success=true
```
Requisição com falha:  
```
http://<localhost>:5000/?success=false
```

5. Para acesar o Prometheus
```
http://<localhost>:9090
```

6. Para acesar o Grafana
```
http://<localhost>:3000
```
Na interface gráfica:  
Email or username: *admin*  
Password: *admin*  

7. Para encerrar a execução dos containers  
```
docker-compose down
```

## **Como foi desenvolvido o projeto**  

**1. Compreensão do conceito/propósito do Prometheus/Grafana**
- Breve leitura dos conceitos de Prometheus/Grafana no artigo ["Monitorando aplicações docker com prometheus e grafana"](https://medium.com/xp-inc/monitorando-aplica%C3%A7%C3%B5es-docker-com-prometheus-e-grafana-593f507fc17) **(Artigo 1)**
- Visto que o artigo trouxe teoria e prática já foi possível partir para o desenvolvimento  

**2. Desenvolvimento de uma aplicação simples em Flask**
- Escolhi Flask pela familiaridade pois foi usado na [Demanda 1](https://github.com/anycarolinys/dockerized_flask_api)
- Utilizei outro artigo com exemplo de aplicação para o Prometheus em Python para compreender as dependências necessárias (["Exposing Python Metrics with Prometheus"](https://medium.com/@letathenasleep/exposing-python-metrics-with-prometheus-c5c837c21e4d)) **(Artigo 2)**
- A aplicação criada foi uma implementação das métricas vistas no Artigo 1 utilizando como base o código do Artigo 2

**3. Desenvolvimento do Dockerfile/Docker Compose**
- Para o Flask utilizei os arquivos da Demanda 1 como base
- Para o Prometheus utilizei como base o compose no Artigo 2, pois no Artigo 1 haviam configurações que eu não julgava serem necessárias a princípio
- Para o Grafana utilizei como base o compose do Artigo 1

**4. Conexão do Prometheus com o Grafana**
- Como a interface do Grafana era intuitiva, bastou usar o Prometheus como fonte de dados adicionando o IP do WSL com a porta 9090 como URL


## **Resultados**
- Prometheus deve estar configurado para coletar métricas do container da
aplicação  
```
scheme: https
    static_configs:
      - targets: ['dockerized-prometheus-grafana.onrender.com']
```

## **Principais dificuldades**  

**1. Métricas configuradas na aplicação Flask não eram exibidas no Prometheus**
- Observei os logs do container do Prometheus e não eram indicados erros
- Fui então testar a aplicação individualmente com ```python app.py``` e não eram exibidos
- Resolvi fazer um teste realizando uma requisição na rota '/' da aplicação e observando os logs de seu container, a partir disso notei um problema com a configuração do método ```labels()```  
- Na [documentação](https://prometheus.github.io/client_python/instrumenting/labels/) (não achei solução em fóruns) tentei compreender o que era necessário nas labels para cada tipo de métrica (Counter, Histogram, Summary)
    -  A documentação sobre o que deveria ser incluído nas labels para cada métrica não era clara e os exemplos eram escassos
    - Utilizei IA para solucionar o problema de configuração das labels, e as métricas passaram a ser exibidas no Prometheus

**2. Deploy de múltiplos serviços com a plataforma Render**
- Utilizei o render para fazer o deploy da Aplicação Flask e é possível acessar a aplicação por [este link](https://dockerized-prometheus-grafana.onrender.com), a plataforma usada (Render) vai manter a URL ativa por mais 750 horas a partir do envio deste projeto
- Não foi possível obter URL de deploy para os serviços do Prometheus e Grafana, eles estão hospedados na plataforma Railway e foram oferecidas variáveis de ambiente como ```RAILWAY_PRIVATE_DOMAIN, RAILWAY_PROJECT_NAME RAILWAY_ENVIRONMENT_NAME,RAILWAY_SERVICE_NAME,RAILWAY_PROJECT_ID RAILWAY_ENVIRONMENT_ID,RAILWAY_SERVICE_ID``` tentei checar se elas formavam uma URL válida juntas mas não existe tal domínio  
    - Para fazer o deploy desses serviços criei dois repositórios separados para o [Prometheus](https://github.com/anycarolinys/prometheus_service) e [Grafana](https://github.com/anycarolinys/grafana_service)
- Sendo assim, [segue o link](https://youtu.be/ilL09HIq-H0?si=4Wk4UgmkDx9xOtlB) de um vídeo de minha autoria demonstrando o funcionamento dos três serviços em conjunto, sendo a API hospedada no Render e o Prometheus/Grafana executados localmente

## **O que poderia ter sido melhorado/realizado com mais tempo**  
- Poderia ter sido realizado o deploy dos serviços Prometheus e Grafana

## **Principais aprendizados**  
- Compreensão dos objetivos das ferramentas Prometheus e Grafana e como elas se comunicam entre si

- Compreensão do uso da API do Prometheus para Python
 
- Compreensão dos dashboards no Grafana, utilizando queries com código ou no builder, configuração de unidades de medida, formatação de legenda e título para o usuário final  ([vídeo utilizado](https://youtu.be/EGgtJUjky8w?si=H2K8y3eOY5DZTysX))


