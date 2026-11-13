from fastapi import APIRouter
from sqlalchemy import select

from app.dependencies import CurrentUser, DbSession
from app.models import Category
from app.schemas import CategoryIn, CategoryOut

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(user: CurrentUser, db: DbSession):
    return db.scalars(select(Category).where(Category.user_id == user.id).order_by(Category.type, Category.name)).all()


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(payload: CategoryIn, user: CurrentUser, db: DbSession):
    category = Category(user_id=user.id, name=payload.name.strip(), type=payload.type)
    db.add(category); db.commit(); db.refresh(category)
    return category
