from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analytics, auth, budgets, categories, imports, transactions
from app.core.config import settings
from app.database import Base, engine
from app import models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FinSight API", version="0.1.0", description="Account-scoped personal spending analytics API")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_url], allow_credentials=True,
                   allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Authorization", "Content-Type"])
app.include_router(auth.router); app.include_router(transactions.router); app.include_router(categories.router)
app.include_router(budgets.router); app.include_router(analytics.router); app.include_router(imports.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "FinSight API"}
