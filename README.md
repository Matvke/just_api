# just_api
RESTful API built with FastAPI for user authentication, post management, and admin operations.

## Features
- JWT token-based authentication
- CRUD operations for posts
- Soft delete with restore functionality
- Role-based access control 

## Installation

1. Install dependencies
`pip install -r requirements.txt`

2. Create .env file
```
DB_HOST= 
DB_PORT= 
DB_USER= 
DB_PASSWORD= 
DB_NAME= 
```

3. Run the application
`uvicorn app.main:app` 

4. Read OpenAPI docs
`http://127.0.0.1:8000/docs`


## Technologies Used
- Python 3.10+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Pydantic (Data validation)
- Alembic (Migrations)
- JWT (Authentication)

## Directory tree
```
api_creater\ 
├── app\                                      # <-- Application Root
│   ├── api\
│   │   └── v1\
│   │       ├── endpoints\                    # <-- v1 endpoints
│   │       │   ├── auth.py
│   │       │   ├── post.py
│   │       │   └── user.py
│   │       └── routes.py                     # <-- Router configs
│   ├── core\                                 # <-- App core configs
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── enums.py
│   │   └── security.py
│   ├── dependencies\                         # <-- Dependency injection
│   │   ├── auth_dependencies.py
│   │   ├── repository_dependencies.py
│   │   └── service_dependencies.py
│   ├── exceptions\                           # <-- Custom exceptions
│   │   ├── exception_handlers.py
│   │   ├── http_exceptions.py
│   │   └── service_exceptions.py
│   ├── model\                                # <-- Database models
│   │   └── models.py
│   ├── repository\                           # <-- Data access layer
│   │   ├── base_repository.py
│   │   ├── post_repository.py
│   │   └── user_repository.py
│   ├── schemas\                              # <-- Pydantic request/response schemas
│   │   ├── auth\
│   │   │   ├── auth_request.py
│   │   │   └── auth_response.py
│   │   ├── post\
│   │   │   ├── post_request.py
│   │   │   └── post_response.py
│   │   └── security_schema.py
│   ├── services\                             # <-- Business logic
│   │   ├── auth_service.py
│   │   ├── post_service.py
│   │   └── user_service.py
│   └── main.py                               # <-- Entry point
├── migration\
├── tests\
├── alembic.ini
├── LICENSE
├── README.md
└── requirements.txt