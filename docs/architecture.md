# FinSight Architecture

The React client calls a FastAPI REST API over HTTPS. FastAPI validates requests, derives the account from a signed expiring JWT, and scopes each database query to that account. SQLAlchemy persists user, category, transaction, and budget records in PostgreSQL (or SQLite during local development).

```text
Browser (React + TypeScript)
        | HTTPS + bearer token
FastAPI routes and validation
        | authenticated account context
Analytics, transaction, budget, and CSV operations
        | SQLAlchemy
PostgreSQL (SQLite for local development)
```

Money totals are computed with database decimal values and returned as verified aggregates. The current CSV flow validates and previews rows before confirmation. It does not connect to financial institutions. The API currently creates tables at startup; production schema evolution should move to Alembic migrations.

## API groups

- `/api/auth`: register, login, current profile
- `/api/transactions`: account-scoped CRUD and search/filter listing
- `/api/categories`: list and create categories
- `/api/budgets`: monthly limits and utilization
- `/api/analytics/overview`: selected-month totals, category expenses, and six-month trend
- `/api/import/csv`: preview and confirm a generic CSV
- `/health`: deployment health check

See the interactive OpenAPI page at `/docs` when running locally.
