# 🚀 SRE-LAB — Plataforma de Observabilidade e Confiabilidade


## 📌 Visão Geral

SRE-LAB é um ambiente de laboratório desenvolvido para praticar conceitos de
Site Reliability Engineering (SRE), DevOps, observabilidade e operação de sistemas.

O projeto simula um ambiente próximo de produção contendo APIs, microsserviços,
monitoramento de métricas, dashboards, alertas e testes de incidentes.

O objetivo principal é aplicar práticas utilizadas por equipes SRE:

- Monitoramento de disponibilidade
- Observabilidade de aplicações
- Análise de performance
- Detecção de falhas
- Resposta a incidentes
- Automação operacional


---

# 🏗️ Arquitetura da Solução


A arquitetura do laboratório é composta por:


```
                 Usuário
                    |
                    v
              Gateway/API
                    |
        -------------------------
        |                       |
        v                       v
Cliente Service          Pedido Service
        |                       |
        -------------------------
                    |
                    v
              PostgreSQL


Aplicações
    |
    v
Métricas Prometheus
    |
    v
Grafana
    |
    v
Alertas SRE
```


---

# 🛠️ Tecnologias Utilizadas


## Aplicação

- Python
- Flask
- API REST


## Infraestrutura

- Docker
- Docker Compose
- Linux


## Banco de Dados

- PostgreSQL


## Observabilidade

- Prometheus
- Grafana
- Prometheus Flask Exporter


## Engenharia

- Git
- Conceitos SRE
- Monitoramento
- Incident Response
- SLIs / SLOs
- Automação


---

# 📂 Estrutura do Projeto


```
SRE-LAB
│
├── apps
│   └── api
│       └── API principal Flask
│
├── services
│   ├── cliente-service
│   │   └── Serviço de clientes
│   │
│   ├── pedido-service
│   │   └── Serviço de pedidos
│   │
│   ├── gateway-api
│   │   └── Gateway da aplicação
│   │
│   └── load-generator
│       └── Geração de tráfego
│
├── monitoring
│   ├── prometheus
│   │   └── Configuração de métricas
│   │
│   └── grafana
│       └── Dashboards e alertas
│
├── database
│   └── postgres
│
├── kubernetes
│
├── terraform
│
├── scripts
│
├── runbooks
│
├── shared
│   └── Código compartilhado
│
├── docker-compose.yml
│
└── Makefile
```


---

# ▶️ Como Executar


## Pré-requisitos


Instalar:

- Docker
- Docker Compose
- Git


## Clonar o projeto


```bash
git clone <repositorio>
cd SRE-LAB
```


## Subir ambiente


```bash
docker compose up -d
```


## Verificar containers


```bash
docker ps
```


Serviços esperados:


- API
- Cliente Service
- Pedido Service
- PostgreSQL
- Prometheus
- Grafana


---

# 🌐 Acessos


## API

```
http://localhost:5000
```


## Prometheus

```
http://localhost:9090
```


## Grafana

```
http://localhost:3000
```


---

# 📊 Observabilidade


O projeto possui monitoramento utilizando Prometheus e Grafana.


## Métricas coletadas


### Disponibilidade

Métrica:

```
up{job="sre-api"}
```


Objetivo:

Verificar se a aplicação está disponível.


---

## Request Rate


Quantidade de requisições por segundo:


```
sum(rate(flask_http_request_total[5m]))
```


Objetivo:

Monitorar volume de tráfego da aplicação.


---

## Latência P95


Métrica utilizada:


```
histogram_quantile(
0.95,
sum(rate(flask_http_request_duration_seconds_bucket[5m])) by (le)
)
```


Objetivo:

Medir experiência do usuário e identificar lentidão.


---

## Error Rate


Percentual de erros HTTP 5xx:


```
(
sum(rate(flask_http_request_total{status=~"5.."}[5m]))
/
sum(rate(flask_http_request_total[5m]))
)
*100
```


Objetivo:

Identificar degradação da aplicação.


---

# 📈 Dashboards Grafana


Dashboard criado:


## SRE-LAB Observability Dashboard


Painéis:


✅ API Availability

✅ API Request Rate

✅ API Latency P95

✅ Cliente Service RPS

✅ Pedido Service RPS

✅ API Error Rate %


---

# 🚨 Alertas SRE Implementados


## API High Error Rate


Objetivo:

Detectar aumento de erros HTTP 500.


Condição:

```
Error Rate > 5%
```


---

## API Down


Objetivo:

Detectar indisponibilidade da aplicação.


Regra:

```
up{job="sre-api"} < 1
```


---

## API High Latency P95


Objetivo:

Detectar degradação de performance.


Condição:

```
P95 > 1 segundo
```


---

# 🔥 Testes de Incidentes Realizados


## Simulação de erro HTTP 500


Foi criada uma rota de teste:


```
GET /erro
```


Resultado:


```
HTTP 500 INTERNAL SERVER ERROR
```


Impacto observado:

- Error Rate aumentou
- Alerta mudou para Pending
- Alerta mudou para Firing


---

## Simulação de indisponibilidade


Container da API foi parado:


```bash
docker stop sre-api
```


Resultado:


- Métrica UP alterada
- Alerta API Down disparado


---

## Simulação de lentidão


Foi adicionada latência artificial na aplicação.


Resultado:


- P95 aumentou
- Alerta de latência validado


---

# 📚 Conceitos SRE Aplicados


Neste projeto foram aplicados:


- Observabilidade
- Monitoramento baseado em métricas
- SLIs
- SLOs
- Alertas inteligentes
- Detecção de incidentes
- Troubleshooting
- Alta disponibilidade
- Cultura DevOps


---

# 🔮 Próximas Melhorias


Possíveis evoluções:


- Integração com Kubernetes
- Deploy utilizando Helm
- Infraestrutura com Terraform
- Logs centralizados com Loki
- Tracing distribuído com OpenTelemetry
- Integração com ferramentas como Datadog e Dynatrace
- Pipeline CI/CD


---


Projeto desenvolvido para estudos práticos de:

**Site Reliability Engineering (SRE)**
**DevOps**
**Cloud Native Observability**
