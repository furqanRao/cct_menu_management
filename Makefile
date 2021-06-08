
dev.ps: ## View list of created services and their statuses.
	docker ps

dev.restart-container: ## Restart all service containers.
	docker restart $$(echo $* | tr + " ")

dev.stop: ## Stop all running services.
	docker-compose stop

dev.down: ## Stop and remove containers and networks for all services.
	docker-compose down

dev.start:
	docker-compose up -d

dev.logs: ## View logs from running containers.
	docker logs -f

dev.logs.%: ## View the logs of the specified service container.
	docker logs -f --tail=500 $*

dev.webshell:
	docker exec -it daily_menu_web_app /bin/bash

dev.dbshell:
	docker exec -it daily_menu_db psql -U postgres

dev.web.makemigrations:
	docker exec -it daily_menu_web_app bash -c "python manage.py makemigrations"

dev.web.runmigrations:
	docker exec -it daily_menu_web_app bash -c "python manage.py migrate"

dev.web.createsuperuser:
	docker exec -it daily_menu_web_app bash -c "python manage.py createsuperuser --noinput"

dev.projectsetup:
	make dev.down
	make dev.start
	sleep 10  # Wait for database to be ready.
	make dev.web.makemigrations
	make dev.web.runmigrations
	make dev.web.createsuperuser
	make dev.stop
	make dev.start

dev.web.tests:          # to run tests
	docker exec -it daily_menu_web_app bash -c "python manage.py test"

