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

- Configure Neon PostgreSQL, production secrets, restrictive CORS, HTTPS, and rate limits.
- Create/push a GitHub repository, connect the hosting accounts, deploy the API to Render and frontend to Vercel, configure `VITE_API_URL`, and verify the live flow with synthetic data.
- Add CI, operational logging that excludes sensitive financial data, backups, screenshots, and deployment instructions.

## Not claimed as complete

Automated tests, live deployment, bank connectivity, machine-learning categorization, anomaly detection, forecasting, recurring payment detection, and AI assistant are not implemented yet.
