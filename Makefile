build:
	docker compose up --build -d

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d

rebuild:
	docker compose up --build -d

logs:
	docker compose logs -f

status:
	docker compose ps

psql:
	docker compose exec -it postgres psql -U postgres -d slides_bot

stamp:
	docker compose exec bot alembic stamp head

revision:
	docker compose exec bot alembic revision --autogenerate

upgrade:
	docker compose exec bot alembic upgrade head

pinggy:
	ssh -p 443 -R0:localhost:8000 qr@free.pinggy.io

ngrok:
	ngrok http 8080
