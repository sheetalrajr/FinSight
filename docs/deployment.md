# Public Deployment

FinSight is configured for a Vercel frontend, a Render API, and a managed PostgreSQL database. A deployment still needs a GitHub repository and signed-in provider accounts. Do not use SQLite or a development secret for a public deployment.

## 1. Create the database

Create a PostgreSQL database with Neon (or another managed PostgreSQL provider). Copy its pooled or direct connection URL into the Render API environment variable `DATABASE_URL`. Keep it private and never put it in a `VITE_` variable.

## 2. Deploy the API on Render

1. Push this project to a GitHub repository.
2. In Render, create a Blueprint from that repository and use the root `render.yaml`.
3. Set the service's `DATABASE_URL` to the managed PostgreSQL connection string.
4. Wait for deployment and check `https://<render-service>.onrender.com/health`.
5. Copy the API origin, without `/health`.

The Blueprint generates `SECRET_KEY`. Keep it private. `FRONTEND_URL` is set after the frontend is deployed.

## 3. Deploy the frontend on Vercel

1. Import the same GitHub repository into Vercel.
2. Set the project Root Directory to `frontend`.
3. Set the environment variable `VITE_API_URL` to the Render API origin, for example `https://finsight-api.onrender.com`.
4. Deploy and copy the resulting `https://<project>.vercel.app` origin.

## 4. Connect the services

Set Render's `FRONTEND_URL` to the exact Vercel production origin, then redeploy the API. The API CORS policy allows that configured origin.

## 5. Verify the public deployment

- Open the Vercel URL in a private browser window and register a synthetic demo account.
- Add income and expense entries, then confirm dashboard totals update.
- Create a budget and test a CSV preview/import.
- Confirm one account cannot access another account's records.
- Check Render logs and the API health endpoint.

The Render web service uses the free plan and may spin down when idle. Free hosted database terms vary by provider; use a paid persistent database for real users or important data. Before broad public use, add rate limits, account recovery, data export/deletion, monitoring, backups, and a privacy policy. Keep demo transactions synthetic.
