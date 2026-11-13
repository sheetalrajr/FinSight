# FinSight Project Overtake

Status snapshot: 2026-11-13

## Done in this workspace

- Established a React/TypeScript frontend and FastAPI backend project layout.
- Implemented account registration/login with password hashing and signed expiring JWTs.
- Added user-scoped transaction CRUD, categories, budgets, overview analytics, and CSV preview/confirmation routes.
- Added deterministic dashboard summaries and charts, transaction listing/entry, budget tracking, and CSV upload preview in the frontend.
- Added environment examples, a synthetic CSV sample, setup documentation, and project conventions.
- Fixed the sign-in form JSX and React/Vite TypeScript declarations; the frontend production build now completes.
- SQLite supports local startup; PostgreSQL URL configuration is supported for hosted use.
- Added Vercel and Render deployment configuration and a deployment guide for managed PostgreSQL.
- Published the project source and deployment configuration to the public `sheetalrajr/FinSight` GitHub repository on `main`.
- Deployed the React frontend and FastAPI backend as public Vercel projects using the free Hobby tier, with Neon Free as the PostgreSQL database.
- Configured encrypted backend environment variables (`DATABASE_URL`, `SECRET_KEY`, and `FRONTEND_URL`) and pointed the frontend's `VITE_API_URL` to the Vercel API.
- Verified API health, browser CORS preflight, and synthetic account registration followed by successful login (201 and 200 responses).
- Added `backend/index.py` as the Vercel FastAPI entry point and updated deployment instructions.

## Needs to be done

### Core quality

- Add automated backend and frontend tests, especially cross-user access, date boundaries, CSV edge cases, and money totals.
- Add database migrations with Alembic and seed default categories for each new user.
- Improve pagination, filtering, transaction editing/deletion, and consistent error handling in the UI.
- Add CSV cross-batch duplicate fingerprints, durable import batches, category correction, and clearer failed-row downloads.
- Add profile/settings, data export/deletion, timezone/currency preferences, and accessibility review.

### Intelligence

- Add transparent merchant categorization rules and a measured text-classification baseline.
- Add unusual-spending flags with minimum-history rules, recurring-payment candidates, and a clearly caveated forecast.
- Add an optional Gemini assistant grounded only in authenticated backend aggregates; handle provider failures and minimize sent data.

### Deployment

- Add rate limits, monitoring, backups, and data export/deletion before broad public use.
- Migrate any user records from the suspended Render service if they need to keep existing accounts; the new Neon database starts empty.
- Add CI, operational logging that excludes sensitive financial data, backups, screenshots, and deployment instructions.

## Not claimed as complete

Automated test suites, bank connectivity, machine-learning categorization, anomaly detection, forecasting, recurring payment detection, and AI assistant are not implemented yet. The prior Render API remains suspended and is no longer used by the live frontend.
