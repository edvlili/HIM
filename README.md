# Home Inventory Management API

A FastAPI-based REST API for managing home inventories with product tracking capabilities.

## Features

- User authentication with JWT tokens
- Home management (CRUD operations)
- Item tracking with categories, quantities, and expiration dates
- Product information lookup by barcode
- Search and filter items by category or text
- PostgreSQL database with SQLAlchemy ORM
- Alembic database migrations

## Requirements

- Python 3.8+
- PostgreSQL 12+
- Make utility

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd home-inventory-management
```

2. Make sure PostgreSQL is running and create a database:
```bash
# Connect to PostgreSQL
psql -U postgres

# In the PostgreSQL prompt, create the database
CREATE DATABASE him_db;
\q
```

3. Run the automated setup:
```bash
make setup-all
```
This command will:
- Create a Python virtual environment
- Install all dependencies
- Set up the environment file (you'll be prompted for database credentials)
- Run database migrations

4. Start the application:
```bash
make run
```

The API will be available at:
- API Endpoints: http://localhost:8000/api/v1
- Interactive API Documentation (Swagger UI): http://localhost:8000/docs

## Development Commands

All commands are available through the Makefile:

- `make setup-all` - Complete project setup (first-time setup)
- `make run` - Start the development server
- `make test` - Run tests
- `make lint` - Check code style
- `make format` - Format code
- `make migrate-up` - Apply database migrations
- `make migrate-down` - Rollback last migration
- `make clean` - Clean up generated files
- `make help` - Show all available commands

## API Endpoints

### Authentication
- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - Login and get access token

### Homes
- GET `/api/v1/homes` - List all homes
- POST `/api/v1/homes` - Create new home
- GET `/api/v1/homes/{home_id}` - Get home details
- PUT `/api/v1/homes/{home_id}` - Update home
- DELETE `/api/v1/homes/{home_id}` - Delete home

### Items
- GET `/api/v1/homes/{home_id}/items` - List all items in home
- POST `/api/v1/homes/{home_id}/items` - Add new item
- GET `/api/v1/homes/{home_id}/items/{item_id}` - Get item details
- PUT `/api/v1/homes/{home_id}/items/{item_id}` - Update item
- DELETE `/api/v1/homes/{home_id}/items/{item_id}` - Delete item

### Product Information
- GET `/api/v1/products/lookup?barcode={barcode}` - Look up product by barcode

## Environment Variables

Create a `.env` file with the following variables:

```env
# Application
PROJECT_NAME=Home Inventory Management API
VERSION=1.0.0
DESCRIPTION="API for managing home inventories with product tracking capabilities"

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/him_db

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 