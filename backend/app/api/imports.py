from datetime import date
from decimal import Decimal, InvalidOperation
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from sqlalchemy import select

from app.dependencies import CurrentUser, DbSession
from app.models import Category, Transaction

router = APIRouter(prefix="/api/import/csv", tags=["CSV import"])
MAX_BYTES = 2_000_000


async def parse_csv(file: UploadFile):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=415, detail="Upload a CSV file")
    contents = await file.read(MAX_BYTES + 1)
    if len(contents) > MAX_BYTES: raise HTTPException(status_code=413, detail="CSV must be smaller than 2 MB")
    try:
        frame = pd.read_csv(BytesIO(contents)).rename(columns=lambda c: str(c).strip().lower())
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Could not read this CSV") from exc
    required = {"date", "description", "amount", "type"}
    if not required.issubset(frame.columns):
        raise HTTPException(status_code=422, detail="CSV needs date, description, amount, type columns")
    rows = []; seen = set()
    for number, row in frame.iterrows():
        errors = []
        try: day = pd.to_datetime(row["date"], errors="raise").date()
        except Exception: day = None; errors.append("Invalid date")
        description = str(row["description"]).strip()
        if not description or description.lower() == "nan": errors.append("Description is required")
        try:
            amount = Decimal(str(row["amount"])).quantize(Decimal("0.01"))
            if not amount.is_finite() or amount <= 0: raise InvalidOperation
        except Exception: amount = Decimal("0.00"); errors.append("Amount must be a positive number")
        kind = str(row["type"]).strip().lower()
        if kind not in ("income", "expense"): errors.append("Type must be income or expense")
        fingerprint = (day, description.lower(), amount, kind)
        duplicate = fingerprint in seen
        seen.add(fingerprint)
        rows.append({"row": int(number)+2, "date": day.isoformat() if day else None, "description": description,
                     "amount": str(amount), "type": kind, "duplicate": duplicate, "errors": errors})
    return rows


@router.post("/preview")
async def preview_csv(user: CurrentUser, file: UploadFile = File(...)):
    rows = await parse_csv(file)
    return {"rows": rows, "valid_count": sum(not r["errors"] and not r["duplicate"] for r in rows),
            "invalid_count": sum(bool(r["errors"]) for r in rows), "duplicate_count": sum(r["duplicate"] for r in rows)}


@router.post("/confirm")
async def confirm_csv(user: CurrentUser, db: DbSession, file: UploadFile = File(...)):
    rows = await parse_csv(file); imported = 0; categories = db.scalars(select(Category).where(Category.user_id == user.id)).all()
    cat_index = {(c.type, c.name.lower()): c for c in categories}
    for row in rows:
        if row["errors"] or row["duplicate"]: continue
        guess = next((c for key, c in cat_index.items() if key[0] == row["type"] and key[1] in row["description"].lower()), None)
        db.add(Transaction(user_id=user.id, transaction_date=date.fromisoformat(row["date"]), description=row["description"],
                           amount=Decimal(row["amount"]), type=row["type"], category_id=guess.id if guess else None))
        imported += 1
    db.commit()
    return {"imported": imported, "skipped": sum(r["duplicate"] for r in rows), "failed": sum(bool(r["errors"]) for r in rows)}
