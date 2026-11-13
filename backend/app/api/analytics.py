from datetime import date
from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import extract, func, select

from app.dependencies import CurrentUser, DbSession
from app.models import Category, Transaction

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview")
def overview(user: CurrentUser, db: DbSession, month: int | None = None, year: int | None = None):
    today = date.today(); month = month or today.month; year = year or today.year
    base = select(Transaction).where(Transaction.user_id == user.id,
        extract("month", Transaction.transaction_date) == month, extract("year", Transaction.transaction_date) == year)
    income = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).where(*base.whereclause.clauses, Transaction.type == "income")) or Decimal("0")
    expenses = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).where(*base.whereclause.clauses, Transaction.type == "expense")) or Decimal("0")
    by_category = db.execute(select(Category.name, func.sum(Transaction.amount)).join(Category, Category.id == Transaction.category_id)
        .where(*base.whereclause.clauses, Transaction.type == "expense").group_by(Category.name).order_by(func.sum(Transaction.amount).desc())).all()
    trend = []
    for offset in range(5, -1, -1):
        idx = year * 12 + month - 1 - offset
        y, m = divmod(idx, 12); m += 1
        vals = db.execute(select(Transaction.type, func.sum(Transaction.amount)).where(Transaction.user_id == user.id,
             extract("month", Transaction.transaction_date) == m, extract("year", Transaction.transaction_date) == y).group_by(Transaction.type)).all()
        totals = {kind: amount for kind, amount in vals}
        trend.append({"month": date(y, m, 1).strftime("%b"), "income": float(totals.get("income") or 0), "expenses": float(totals.get("expense") or 0)})
    return {"month": month, "year": year, "income": float(income), "expenses": float(expenses), "net_cash_flow": float(income - expenses),
            "savings_rate": float((income-expenses)/income*100) if income > 0 else None,
            "categories": [{"name": name or "Uncategorized", "amount": float(amount)} for name, amount in by_category], "trend": trend}
