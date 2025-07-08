from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    amount: float
    transaction_type: str  # "income" or "expense"
    category: Optional[str] = None
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    user_id: int

class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TransactionSummary(BaseModel):
    total_income: float
    total_expenses: float
    balance: float
    transaction_count: int

class UserSummary(BaseModel):
    user_id: int
    summary: TransactionSummary 