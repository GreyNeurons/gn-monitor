start-pgsql:
	docker start gn-monitor-pgsql || docker run -d -v $(pwd)/.docker:/docker-entrypoint-initdb.d -e POSTGRES_PASSWORD=PgPass -p 5432:5432 --name gn-monitor-pgsql postgres:16.2-alpine

clean-pgsql: stop-pgsql
	@docker rm gn-monitor-pgsql || true

stop-pgsql:
	@docker stop gn-monitor-pgsql || true

start-devserver: start-pgsql
    @cd src && fastapi dev main.py

test:
	@cd src && pytest

lint:
	@ruff check --fix
