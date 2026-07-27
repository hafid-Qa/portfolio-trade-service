

help:
	@printf "Targets:\n"
	@printf "  up      Build and run the container\n"
	@printf "  test                 Run tests using pytest\n"
 


up: ## build and run the container
	docker compose up

test: ## run test
	docker compose  run --rm  test ruff check .
	docker compose  run --rm  test pytest
