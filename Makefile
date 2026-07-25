# ===========================
# SRE LAB
# Makefile
# ===========================


COMPOSE=docker compose --env-file .env -f docker/ambiente-inicial/docker-compose.yml



up:
	$(COMPOSE) up -d



down:
	$(COMPOSE) down



restart:
	$(COMPOSE) down
	$(COMPOSE) up -d



build:
	$(COMPOSE) build



logs:
	$(COMPOSE) logs -f



ps:
	$(COMPOSE) ps



pull:
	$(COMPOSE) pull



clean:
	$(COMPOSE) down -v
	docker system prune -f



status:
	docker ps
