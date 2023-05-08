pip-install-dev:
	pip install --upgrade pip pip-tools
	pip-sync src/requirements-dev.txt

pip-install:
	pip install --upgrade pip pip-tools
	pip-sync src/requirements.txt

pip-update:
	pip install --upgrade pip pip-tools
	pip-compile requirements/base.in -o src/requirements.txt
	pip-compile requirements/dev.in -o src/requirements-dev.txt
	pip-sync src/requirements.txt src/requirements-dev.txt

build-server:
	docker-compose up -d --build

server:
	docker-compose up

down-server:
	docker-compose down