PHONY: help

SHELL := /bin/bash

.DEFAULT_GOAL := help


help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

create_secrets: ## create TLS certificates
	./create_secrets.sh

trino_shell: ## spawn trino shell
	docker exec -it trino-cli /bin/trino --server trino:8080 --catalog iceberg --schema default

airflow_shell: ## spawn airflow shell
	docker exec -it airflow-scheduler /bin/bash

postgresql_shell: ## spawn postgresql shell
	docker exec -it db-pg bash -c 'psql -U $POSTGRES_USER $POSTGRES_PASSWORD -d example' 

mongodb_shell: ## spawn mongodb shell
	docker exec -it db-mongo bash -c 'mongosh --host db-mongo --port 27017'                                                                                                                      │

debezium_logs: ## tail debezium connect logs
	docker logs debezium-connect -f

############################################################
compose_cdc_build: ## CDC compose build images
	docker compose -f docker compose.yml -f docker compose_cdc.yml build

compose_cdc: ## CDC compose up
	docker compose -f docker compose.yml -f docker compose_cdc.yml up -d

compose_cdc_down: ## CDC compose down (without data purge)
	docker compose -f docker compose.yml -f docker compose_cdc.yml down

compose_cdc_downclean: ## CDC compose down and purge
	docker compose -f docker compose.yml -f docker compose_cdc.yml down -v

############################################################
compose_batch_build: ## Batch mode compose build images
	docker compose -f docker compose.yml -f docker compose-airflow.yml build

compose_batch: ## Batch mode compose up
	docker compose -f docker compose.yml -f docker compose-airflow.yml up -d

compose_batch_down: ## Batch mode compose down (without data purge)
	docker compose -f docker compose.yml -f docker compose-airflow.yml down

compose_batch_downclean: ## Batch mode compose down and purge
	docker compose -f docker compose.yml -f docker compose-airflow.yml down -v

