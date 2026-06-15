# Database migrations

Generate a new migration after changing models:

```bash
alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```bash
alembic upgrade head
```

Roll back the last migration:

```bash
alembic downgrade -1
```
