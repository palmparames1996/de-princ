help :
	@echo "help"

local-config:
	cp local.env .env

local-start:
	docker-compose -f local-docker-compose.yml up -d

local-build:
	docker-compose -f local-docker-compose.yml up -d --build

local-stop:
	docker-compose -f local-docker-compose.yml down