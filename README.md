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
- Poetry (optional, for dependency management)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd home-inventory-management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database and update the connection string in `.env`:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run database migrations:
```bash
make migrate
```

## Running the Application

Start the development server:
```bash
make run
```

The API will be available at http://localhost:8000/api/v1

API documentation (Swagger UI) will be available at http://localhost:8000/docs

## Development

- Run tests: `make test`
- Format code: `make lint`
- Create new migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `make migrate`
- Rollback migrations: `make migrate-down`

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