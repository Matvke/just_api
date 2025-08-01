# just_api
Just fastapi clean architecture.

# Directory tree
```
api_creater\ 
├── app\
│   ├── api\
│   │   └── v1\
│   │       ├── endpoints\
│   │       │   ├── auth.py
│   │       │   ├── post.py
│   │       │   └── user.py
│   │       └── routes.py
│   ├── core\
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── enums.py
│   │   └── security.py
│   ├── dependencies\
│   │   ├── auth_dependencies.py
│   │   ├── repository_dependencies.py
│   │   └── service_dependencies.py
│   ├── exceptions\
│   │   ├── exception_handlers.py
│   │   ├── http_exceptions.py
│   │   └── service_exceptions.py
│   ├── model\
│   │   └── models.py
│   ├── repository\
│   │   ├── base_repository.py
│   │   ├── post_repository.py
│   │   └── user_repository.py
│   ├── schemas\
│   │   ├── auth\
│   │   │   ├── auth_request.py
│   │   │   └── auth_response.py
│   │   ├── post\
│   │   │   ├── post_request.py
│   │   │   └── post_response.py
│   │   └── security_schema.py
│   ├── services\
│   │   ├── auth_service.py
│   │   ├── post_service.py
│   │   └── user_service.py
│   └── main.py
├── migration\
├── tests\
├── alembic.ini
├── LICENSE
├── README.md
└── requirements.txt