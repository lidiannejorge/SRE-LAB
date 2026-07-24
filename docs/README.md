# 🚀 SRE LAB

Laboratório prático para estudo de Site Reliability Engineering (SRE), DevOps e Observabilidade.

Este projeto simula um ambiente de produção utilizando Docker, Nginx, Flask, Prometheus e Grafana para monitoramento de serviços.

---

## Objetivos

- Aprender Docker e Docker Compose
- Implementar Health Checks
- Monitorar aplicações com Prometheus
- Criar dashboards no Grafana
- Simular ambientes reais utilizados por equipes SRE
- Documentar procedimentos operacionais (Runbooks)

---

## Tecnologias

- Docker
- Docker Compose
- Python 3
- Flask
- Nginx
- Prometheus
- Grafana
- Git
- GitHub

---

## Estrutura do Projeto

```text
SRE-LAB
├── apps/
├── docker/
├── docs/
├── kubernetes/
├── monitoring/
├── runbooks/
├── scripts/
└── terraform/
```

---

## Arquitetura

```
          Usuário
             │
             ▼
          Nginx
             │
             ▼
         Flask API
             │
      ┌──────┴──────┐
      ▼             ▼
Prometheus      Health Check
      │
      ▼
   Grafana
```

---

## Como executar

Clone o projeto:

```bash
git clone git@github.com:lidiannejorge/SRE-LAB.git
```

Entre na pasta:

```bash
cd SRE-LAB
```

Inicie os containers:

```bash
docker compose up -d
```

Verifique os serviços:

```bash
docker ps
```

---

## Funcionalidades

- API Flask
- Endpoint `/health`
- Monitoramento com Prometheus
- Dashboards Grafana
- Containers Docker
- Health Checks

---

## Roadmap

- [x] Docker
- [x] Docker Compose
- [x] API Flask
- [ ] Prometheus
- [ ] Grafana
- [ ] Loki
- [ ] Promtail
- [ ] Kubernetes
- [ ] GitHub Actions
- [ ] Terraform

---
