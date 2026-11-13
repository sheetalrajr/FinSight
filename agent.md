# Agent Guide

## Product rules

- FinSight is a personal finance analytics and learning tool, not a bank, investment adviser, credit product, or fraud-detection service.
- Money math belongs in deterministic backend services and uses decimal values. Never ask a language model to calculate totals or execute arbitrary SQL.
- Never trust a browser-supplied user ID. Derive ownership from the validated token and scope every private query to that user.
- Keep provider keys and secrets on the server. Never expose backend secrets through `VITE_` variables.
- CSV files are untrusted input. Validate format, size, required fields, dates, amounts, and types before committing rows.
- Use neutral language for unusual activity; an anomaly is not proof of fraud.

## Structure

- `frontend/src`: React pages, reusable components, API client, and types.
- `backend/app/api`: HTTP routes; keep handlers thin.
- `backend/app/models`: SQLAlchemy persistence models.
- `backend/app/schemas`: validated request and response models.
- `backend/app/services`: authentication, analytics, CSV, and business logic.
- `sample_data`: synthetic CSV examples only.

## Change conventions

- Keep API contracts typed and errors understandable.
- Preserve account-level isolation on every read, update, and delete.
- Store timestamps in UTC and use ISO dates in API payloads.
- Add dependency versions to dependency files and keep `.env` files out of source control.
- Update `overtake.md` when project work changes; claims about completed features must match the code.
- Do not claim tests, deployment, AI, or ML are complete without evidence.
