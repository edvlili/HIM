.PHONY: setup clean install run test lint format migrate docker-build docker-run docs env-create env-remove

# Environment settings
ENV_NAME = HIM
PYTHON_VERSION = 3.8
PYTHON = python3
VIRTUALENV = venv

# Project settings
VENV_DIR = $(ENV_NAME)
BIN = $(VENV_DIR)/bin
APP = app
MIGRATIONS = alembic/versions

# Docker settings
DOCKER_IMAGE = home-inventory-api
DOCKER_TAG = latest

# Default target
all: setup

# Create virtualenv environment
env-create:
	@echo "Creating virtualenv environment: $(ENV_NAME)"
	@if ! command -v $(VIRTUALENV) >/dev/null 2>&1; then \
		echo "Installing virtualenv..."; \
		$(PYTHON) -m pip install virtualenv; \
	fi
	@$(PYTHON) -m $(VIRTUALENV) $(ENV_NAME)
	@echo "Activating environment and installing dependencies..."
	@. $(ENV_NAME)/bin/activate && pip install --upgrade pip
	@. $(ENV_NAME)/bin/activate && pip install -r requirements.txt
	@echo "Environment $(ENV_NAME) created successfully"
	@echo "To activate the environment, run: source $(ENV_NAME)/bin/activate"

# Remove virtualenv environment
env-remove:
	@echo "Removing virtualenv environment: $(ENV_NAME)"
	rm -rf $(ENV_NAME)

# Install project dependencies
install:
	@echo "Installing dependencies..."
	@. $(ENV_NAME)/bin/activate && pip install -r requirements.txt

# Run the application in development mode
run:
	@echo "Starting development server..."
	@. $(ENV_NAME)/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	@echo "Running tests..."
	@. $(ENV_NAME)/bin/activate && pytest -v --cov=$(APP) --cov-report=term-missing

# Run linting
lint:
	@echo "Running linters..."
	@. $(ENV_NAME)/bin/activate && flake8 $(APP)
	@. $(ENV_NAME)/bin/activate && mypy $(APP)
	@. $(ENV_NAME)/bin/activate && black $(APP) --check
	@. $(ENV_NAME)/bin/activate && isort $(APP) --check-only

# Format code
format:
	@echo "Formatting code..."
	@. $(ENV_NAME)/bin/activate && black $(APP)
	@. $(ENV_NAME)/bin/activate && isort $(APP)

# Database migrations
migrate-init:
	@echo "Initializing migrations..."
	@. $(ENV_NAME)/bin/activate && alembic init $(MIGRATIONS)

migrate-create:
	@echo "Creating new migration..."
	@. $(ENV_NAME)/bin/activate && alembic revision --autogenerate -m "$(message)"

migrate-up:
	@echo "Applying migrations..."
	@. $(ENV_NAME)/bin/activate && alembic upgrade head

migrate-down:
	@echo "Rolling back migration..."
	@. $(ENV_NAME)/bin/activate && alembic downgrade -1

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run:
	@echo "Running Docker container..."
	docker run -p 8000:8000 --env-file .env $(DOCKER_IMAGE):$(DOCKER_TAG)

# Generate documentation
docs:
	@echo "Generating documentation..."
	@. $(ENV_NAME)/bin/activate && pdoc --html $(APP) --output-dir docs

# Clean up generated files and virtual environment
clean:
	@echo "Cleaning up..."
	rm -rf $(ENV_NAME)
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

# Help target
help:
	@echo "Available targets:"
	@echo "  env-create    : Create virtualenv environment named $(ENV_NAME)"
	@echo "  env-remove    : Remove virtualenv environment"
	@echo "  install      : Install project dependencies"
	@echo "  run          : Run development server"
	@echo "  test         : Run tests"
	@echo "  lint         : Run linters"
	@echo "  format       : Format code"
	@echo "  migrate-init : Initialize database migrations"
	@echo "  migrate-create: Create new migration (use with message='')"
	@echo "  migrate-up   : Apply migrations"
	@echo "  migrate-down : Rollback last migration"
	@echo "  docker-build : Build Docker image"
	@echo "  docker-run   : Run Docker container"
	@echo "  docs         : Generate documentation"
	@echo "  clean        : Clean up generated files" 