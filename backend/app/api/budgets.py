from datetime import date
from decimal import Decimal

from fastapi import APIRouter, HTTPException
from sqlalchemy import extract, func, select
from sqlalchemy.orm import joinedload

from app.dependencies import CurrentUser, DbSession
from app.models import Budget, Category, Transaction
from app.schemas import BudgetIn, BudgetOut

router = APIRouter(prefix="/api/budgets", tags=["budgets"])


@router.get("", response_model=list[dict])
def list_budgets(user: CurrentUser, db: DbSession, month: int | None = None, year: int | None = None):
    today = date.today(); month = month or today.month; year = year or today.year
    rows = db.scalars(select(Budget).options(joinedload(Budget.category)).where(Budget.user_id == user.id, Budget.month == month, Budget.year == year)).unique().all()
    result = []
    for row in rows:
        spent = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user.id, Transaction.category_id == row.category_id, Transaction.type == "expense",
            extract("month", Transaction.transaction_date) == month, extract("year", Transaction.transaction_date) == year)) or Decimal("0")
        result.append({"id": row.id, "category_id": row.category_id, "category": {"id": row.category.id, "name": row.category.name, "type": row.category.type},
                       "monthly_limit": row.monthly_limit, "month": month, "year": year, "spent": spent,
                       "utilization": float(spent / row.monthly_limit * 100) if row.monthly_limit else 0})
    return result


@router.post("", response_model=BudgetOut, status_code=201)
def upsert_budget(payload: BudgetIn, user: CurrentUser, db: DbSession):
    category = db.scalar(select(Category).where(Category.id == payload.category_id, Category.user_id == user.id, Category.type == "expense"))
    if not category: raise HTTPException(status_code=422, detail="Budget category must be one of your expense categories")
    row = db.scalar(select(Budget).where(Budget.user_id == user.id, Budget.category_id == category.id, Budget.month == payload.month, Budget.year == payload.year))
    if row: row.monthly_limit = payload.monthly_limit
    else:
        row = Budget(user_id=user.id, **payload.model_dump()); db.add(row)
    db.commit()
    return db.scalar(select(Budget).options(joinedload(Budget.category)).where(Budget.id == row.id))
