# FinSight

FinSight is a personal spending analyzer built around reliable transaction data. This MVP includes a React/TypeScript dashboard and a FastAPI backend with account registration, JWT authentication, transactions, categories, budgets, CSV preview/import, and deterministic analytics.

## Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, Recharts
- Backend: Python, FastAPI, SQLAlchemy, Pydantic, Pandas
- Database: PostgreSQL in deployment; SQLite is supported for local development

## Run locally

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; OpenAPI docs are at `/docs`.

### Frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Set `VITE_API_URL` to the API origin (default: `http://127.0.0.1:8000`). Create a user from the Register screen. Financial values are stored as decimal amounts and calculated by the backend. The demo uses synthetic records entered by the user; it does not connect to banks.

## CSV format

Upload a CSV with `date,description,amount,type` columns. Dates should be ISO `YYYY-MM-DD`, amounts positive decimal values, and type `income` or `expense`. Preview validation runs before import. The current MVP skips exact matching duplicates within the uploaded batch; importing across separate batches may still create duplicates.

## Security and limitations

Passwords are hashed, private API endpoints require a signed expiring JWT, and records are filtered by the authenticated user. Configure a strong `SECRET_KEY`, HTTPS, production CORS, database backups, rate limits, and account export/deletion before public deployment. AI, machine-learning classification, recurring detection, forecasting, migrations, and production deployment are not yet implemented. Nothing in the app is financial advice.

See [overtake.md](overtake.md) for implementation status and [agent.md](agent.md) for project conventions.
For hosting setup, follow [docs/deployment.md](docs/deployment.md).
