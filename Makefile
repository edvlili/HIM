.PHONY: setup clean install run test lint format migrate docker-build docker-run docs

# Python and virtualenv settings
PYTHON = python3
VENV = venv
BIN = $(VENV)/bin
APP = src/app
MIGRATIONS = src/app/db/migrations

# Docker settings
DOCKER_IMAGE = home-inventory-api
DOCKER_TAG = latest

# Default target
all: setup

# Create virtual environment and install dependencies
setup: clean
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt
	cp .env.example .env
	$(BIN)/pre-commit install

# Install project dependencies
install:
	$(BIN)/pip install -r requirements.txt

# Run the application in development mode
run:
	$(BIN)/uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	$(BIN)/pytest -v --cov=$(APP) --cov-report=term-missing

# Run linting
lint:
	$(BIN)/flake8 $(APP)
	$(BIN)/mypy $(APP)
	$(BIN)/black $(APP) --check
	$(BIN)/isort $(APP) --check-only

# Format code
format:
	$(BIN)/black $(APP)
	$(BIN)/isort $(APP)

# Database migrations
migrate-init:
	$(BIN)/alembic init $(MIGRATIONS)

migrate-create:
	$(BIN)/alembic revision --autogenerate -m "$(message)"

migrate-up:
	$(BIN)/alembic upgrade head

migrate-down:
	$(BIN)/alembic downgrade -1

# Docker commands
docker-build:
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run:
	docker run -p 8000:8000 --env-file .env $(DOCKER_IMAGE):$(DOCKER_TAG)

# Generate documentation
docs:
	$(BIN)/pdoc --html $(APP) --output-dir docs

# Clean up generated files and virtual environment
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "docs" -exec rm -rf {} + 