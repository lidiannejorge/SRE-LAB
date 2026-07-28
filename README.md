# 🚀 SRE-LAB — Plataforma de Observabilidade e Engenharia de Confiabilidade

Projeto desenvolvido para demonstrar conceitos e práticas de **Site Reliability Engineering (SRE)**, incluindo monitoramento, observabilidade, métricas, logs, distributed tracing, containers e análise de incidentes.

O objetivo do laboratório é simular um ambiente real de produção com múltiplos serviços, permitindo acompanhar:

* Disponibilidade das aplicações
* Performance dos serviços
* Erros e falhas
* Dependências entre microsserviços
* Rastreamento distribuído de requisições
* Monitoramento com ferramentas utilizadas no mercado

---

# 📌 Arquitetura do Projeto

A arquitetura é baseada em microsserviços executando em containers Docker.

```
                         Usuário
                            |
                            |
                            v

                     +-------------+
                     |   sre-api   |
                     |   Flask     |
                     |   :5000     |
                     +-------------+
                            |
          +-----------------+-----------------+
          |                                   |
          v                                   v

+----------------------+          +----------------------+
| cliente-service      |          | pedido-service       |
| Flask                |          | Flask                |
| :5001                |          | :5002                |
+----------------------+          +----------------------+
          |                                   |
          v                                   v

       PostgreSQL                         PostgreSQL


                    Observabilidade

                            |
                            v

        +--------------------------------+
        | OpenTelemetry Collector        |
        +--------------------------------+
                 |
        +--------+---------+
        |                  |
        v                  v

   Dynatrace            Jaeger


        +--------------------------------+
        | Prometheus                     |
        | Grafana                        |
        | Loki                           |
        | Promtail                       |
        +--------------------------------+
```

---

# 🏗️ Serviços da Aplicação

## sre-api

Serviço principal responsável por receber chamadas e encaminhar para os microsserviços.

Porta:

```
5000
```

Endpoints:

```
GET /
GET /health
GET /users
GET /clientes
GET /pedidos
GET /erro
GET /metrics
```

Responsabilidades:

* API Gateway simples
* Comunicação entre serviços
* Geração de traces distribuídos
* Exposição de métricas

---

## cliente-service

Microsserviço responsável pelo gerenciamento de clientes.

Porta:

```
5001
```

Endpoint:

```
GET /clientes
```

Exemplo de resposta:

```json
[
  {
    "id":1,
    "nome":"Cliente Teste",
    "email":"teste@email.com"
  }
]
```

---

## pedido-service

Microsserviço responsável pelos pedidos.

Porta:

```
5002
```

Endpoint:

```
GET /pedidos
```

Exemplo:

```json
[
  {
    "id":1,
    "produto":"Notebook",
    "valor":3500
  }
]
```

---

# 🐳 Containerização

Todos os serviços são executados utilizando Docker Compose.

Serviços:

```
sre-api
sre-cliente-service
sre-pedido-service
sre-postgres
sre-prometheus
sre-grafana
sre-loki
sre-promtail
sre-otel-collector
sre-jaeger
sre-node-exporter
```

Comando para iniciar:

```bash
docker compose up -d
```

Verificar containers:

```bash
docker ps
```

---

# 📊 Observabilidade

O projeto implementa os três pilares da observabilidade:

## 1. Métricas

Ferramentas:

* Prometheus
* Grafana
* Node Exporter

Métricas coletadas:

* Quantidade de requisições
* Status HTTP
* Tempo de resposta
* Uso de recursos

Exemplos:

```
flask_http_request_total

cliente_service_requests_total

pedido_service_requests_total
```

---

# 🔎 Distributed Tracing

Implementado utilizando:

* OpenTelemetry
* OTLP
* Dynatrace
* Jaeger

Exemplo de rastreamento:

```
GET /clientes

        |
        v

sre-api

        |
        v

call-cliente-service

        |
        v

cliente-service

        |
        v

listar-clientes
```

Exemplo no Dynatrace:

```
GET /clientes

Duration:
32 ms

Status:
200
```

---

Outro fluxo:

```
GET /pedidos

        |
        v

sre-api

        |
        v

call-pedido-service

        |
        v

pedido-service

        |
        v

listar-pedidos
```

---

# 🚨 Simulação de Incidentes

O endpoint:

```
GET /erro
```

simula uma falha de aplicação.

Resposta:

```json
{
 "error":"Erro simulado SRE para teste de observabilidade",
 "status":"FAILED"
}
```

O Dynatrace identifica:

```
Endpoint:
GET /erro

Service:
sre-api

Status:
500 Failure
```

Esse cenário representa:

* Detecção de incidente
* Investigação
* Análise de causa
* Monitoramento de impacto

---

# 📈 SRE Practices Implementadas

## Monitoramento

Implementado:

✅ Health checks
✅ Métricas de aplicação
✅ Monitoramento de containers
✅ Traces distribuídos

---

## SLIs

Indicadores acompanhados:

### Disponibilidade

Exemplo:

```
Requests bem sucedidos / Total de requests
```

---

### Taxa de erro

Objetivo:

```
Erro HTTP 5xx < 1%
```

---

### Latência

Monitoramento:

```
Tempo de resposta
p95
p99
```

---

# 🛠️ Tecnologias Utilizadas

## Backend

* Python
* Flask
* REST API

## Observabilidade

* Dynatrace
* OpenTelemetry
* Prometheus
* Grafana
* Loki
* Promtail
* Jaeger

## Infraestrutura

* Docker
* Docker Compose
* PostgreSQL

## Conceitos SRE

* Observability
* Distributed Tracing
* Monitoring
* Incident Management
* Reliability Engineering
* SLI / SLO
* Error Budget
* Troubleshooting

---

# 📂 Estrutura do Projeto

```
SRE-LAB/

├── apps/
│   └── api/
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
│

├── services/

│   ├── cliente-service/
│   │   ├── app.py
│   │   └── Dockerfile
│
│   └── pedido-service/
│       ├── app.py
│       └── Dockerfile
│

├── monitoring/

│   ├── prometheus/
│   ├── grafana/
│   ├── loki/
│   └── promtail/

│

├── docker-compose.yml

└── README.md
```

---

# ▶️ Executando o Projeto

Clonar:

```bash
git clone <repositorio>
```

Entrar no projeto:

```bash
cd SRE-LAB
```

Subir ambiente:

```bash
docker compose up -d --build
```

Verificar:

```bash
docker ps
```

---

# 🧪 Testes

API:

```bash
curl http://localhost:5000
```

Clientes:

```bash
curl http://localhost:5000/clientes
```

Pedidos:

```bash
curl http://localhost:5000/pedidos
```

Erro:

```bash
curl http://localhost:5000/erro
```

---

# 🎯 Objetivo Profissional

Este laboratório demonstra conhecimentos aplicados em:

* Analista SRE Jr
* DevOps
* Cloud Operations
* Monitoramento de aplicações
* Troubleshooting
* Observabilidade moderna

O projeto simula um ambiente real onde um profissional SRE precisa:

1. Monitorar sistemas
2. Detectar problemas
3. Investigar impactos
4. Encontrar causa raiz
5. Melhorar confiabilidade

--

**Site Reliability Engineering (SRE)**
**Observabilidade**
**Cloud Native**
**DevOps**
