from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import CurrentUser, DbSession
from app.models import Category, User
from app.schemas import Login, Token, UserCreate, UserOut
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=Token, status_code=201)
def register(payload: UserCreate, db: DbSession):
    email = payload.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(name=payload.name.strip(), email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.flush()
    defaults = {
        "expense": ["Food & Dining", "Transportation", "Shopping", "Entertainment", "Education", "Healthcare", "Rent", "Utilities", "Other"],
        "income": ["Salary", "Freelancing", "Gifts", "Interest", "Other"],
    }
    db.add_all([Category(user_id=user.id, name=name, type=kind) for kind, names in defaults.items() for name in names])
    db.commit()
    db.refresh(user)
    return {"access_token": create_access_token(user.id), "user": user}


@router.post("/login", response_model=Token)
def login(payload: Login, db: DbSession):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    return {"access_token": create_access_token(user.id), "user": user}


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user
