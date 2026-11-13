from datetime import date

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.dependencies import CurrentUser, DbSession
from app.models import Category, Transaction
from app.schemas import TransactionIn, TransactionOut

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


def owned_category(db, category_id: str | None, user_id: str, kind: str):
    if category_id is None:
        return None
    category = db.scalar(select(Category).where(Category.id == category_id, Category.user_id == user_id))
    if not category or category.type != kind:
        raise HTTPException(status_code=422, detail="Choose a category matching this transaction type")
    return category.id


@router.get("", response_model=list[TransactionOut])
def list_transactions(user: CurrentUser, db: DbSession, start: date | None = None, end: date | None = None,
                      category_id: str | None = None, kind: str | None = Query(default=None, alias="type"),
                      search: str | None = None, offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    q = select(Transaction).options(joinedload(Transaction.category)).where(Transaction.user_id == user.id)
    if start: q = q.where(Transaction.transaction_date >= start)
    if end: q = q.where(Transaction.transaction_date <= end)
    if category_id: q = q.where(Transaction.category_id == category_id)
    if kind in ("income", "expense"): q = q.where(Transaction.type == kind)
    if search: q = q.where(Transaction.description.ilike(f"%{search[:100]}%"))
    return db.scalars(q.order_by(Transaction.transaction_date.desc(), Transaction.created_at.desc()).offset(offset).limit(limit)).unique().all()


@router.post("", response_model=TransactionOut, status_code=201)
def create_transaction(payload: TransactionIn, user: CurrentUser, db: DbSession):
    category_id = owned_category(db, payload.category_id, user.id, payload.type)
    row = Transaction(**payload.model_dump(exclude={"category_id"}), category_id=category_id, user_id=user.id)
    db.add(row); db.commit(); db.refresh(row)
    return db.scalar(select(Transaction).options(joinedload(Transaction.category)).where(Transaction.id == row.id))


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: str, user: CurrentUser, db: DbSession):
    row = db.scalar(select(Transaction).options(joinedload(Transaction.category)).where(Transaction.id == transaction_id, Transaction.user_id == user.id))
    if not row: raise HTTPException(status_code=404, detail="Transaction not found")
    return row


@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(transaction_id: str, payload: TransactionIn, user: CurrentUser, db: DbSession):
    row = db.scalar(select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user.id))
    if not row: raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in payload.model_dump().items(): setattr(row, key, value)
    row.category_id = owned_category(db, payload.category_id, user.id, payload.type)
    db.commit()
    return db.scalar(select(Transaction).options(joinedload(Transaction.category)).where(Transaction.id == row.id))


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: str, user: CurrentUser, db: DbSession):
    row = db.scalar(select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user.id))
    if not row: raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(row); db.commit()
