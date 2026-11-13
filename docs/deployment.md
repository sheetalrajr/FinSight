# Public Deployment

FinSight uses Vercel for the frontend and FastAPI API, with Neon PostgreSQL for persistent data. The Render Blueprint remains available as an alternative API host. Do not use SQLite or a development secret for a public deployment.

## 1. Create the database

Create a PostgreSQL database with Neon (or another managed PostgreSQL provider). Copy its pooled connection URL into the API project's `DATABASE_URL` environment variable. Keep it private and never put it in a `VITE_` variable.

## 2. Deploy the API on Vercel

1. Create a Vercel project for this repository with the Root Directory set to `backend`.
2. Set `DATABASE_URL` to the Neon pooled PostgreSQL connection string.
3. Set `SECRET_KEY` to a long, random private value.
4. Set `FRONTEND_URL` to the public frontend origin.
5. Wait for deployment and check `https://<api-project>.vercel.app/health`.
6. Use the API project origin as the frontend's `VITE_API_URL`.

Vercel detects the FastAPI application through `backend/index.py` and `backend/requirements.txt`.

## 3. Deploy the frontend on Vercel

The frontend Vercel project uses Root Directory `frontend`. Set `VITE_API_URL` to the API project's origin, then deploy and copy the resulting `https://<project>.vercel.app` origin.

## 4. Connect the services

Set the API project's `FRONTEND_URL` to the exact Vercel production origin, then redeploy the API. The API CORS policy allows that configured origin.

## 5. Verify the public deployment

- Open the Vercel frontend URL in a private browser window and register a synthetic demo account.
- Add income and expense entries, then confirm dashboard totals update.
- Create a budget and test a CSV preview/import.
- Confirm one account cannot access another account's records.
- Check Vercel function logs and the API health endpoint.

Vercel Hobby functions and Neon Free have usage limits and availability rules that may change. Before broad public use, add rate limits, account recovery, data export/deletion, monitoring, backups, and a privacy policy. Keep demo transactions synthetic.
