from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)


class Login(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TransactionIn(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    type: Literal["income", "expense"]
    description: str = Field(min_length=1, max_length=240)
    category_id: str | None = None
    merchant: str | None = Field(default=None, max_length=120)
    transaction_date: date


class CategoryOut(BaseModel):
    id: str
    name: str
    type: str
    model_config = ConfigDict(from_attributes=True)


class TransactionOut(BaseModel):
    id: str
    amount: Decimal
    type: str
    description: str
    category_id: str | None
    merchant: str | None
    transaction_date: date
    category: CategoryOut | None = None
    model_config = ConfigDict(from_attributes=True)


class CategoryIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    type: Literal["income", "expense"]


class BudgetIn(BaseModel):
    category_id: str
    monthly_limit: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2200)


class BudgetOut(BaseModel):
    id: str
    category_id: str
    monthly_limit: Decimal
    month: int
    year: int
    category: CategoryOut
    model_config = ConfigDict(from_attributes=True)
