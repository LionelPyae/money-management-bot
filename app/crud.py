from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import List, Optional
from datetime import datetime, timedelta

def create_transaction(db: Session, transaction: schemas.TransactionCreate) -> models.Transaction:
    """Create a new transaction"""
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions_by_user(db: Session, user_id: int, limit: int = 10) -> List[models.Transaction]:
    """Get recent transactions for a user"""
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id
    ).order_by(models.Transaction.created_at.desc()).limit(limit).all()

def get_transactions_by_user_and_period(
    db: Session, 
    user_id: int, 
    days: int = 30
) -> List[models.Transaction]:
    """Get transactions for a user within a specific time period"""
    start_date = datetime.now() - timedelta(days=days)
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.created_at >= start_date
    ).order_by(models.Transaction.created_at.desc()).all()

def get_user_summary(db: Session, user_id: int, days: int = 30) -> schemas.TransactionSummary:
    """Get financial summary for a user within a specific time period"""
    start_date = datetime.now() - timedelta(days=days)
    
    # Get transactions within the period
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.created_at >= start_date
    ).all()
    
    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == "expense")
    balance = total_income - total_expenses
    
    return schemas.TransactionSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        transaction_count=len(transactions)
    )

def get_category_summary(db: Session, user_id: int, days: int = 30) -> dict:
    """Get expense summary by category"""
    start_date = datetime.now() - timedelta(days=days)
    
    # Get expenses grouped by category
    category_expenses = db.query(
        models.Transaction.category,
        func.sum(models.Transaction.amount).label('total')
    ).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.transaction_type == "expense",
        models.Transaction.created_at >= start_date,
        models.Transaction.category.isnot(None)
    ).group_by(models.Transaction.category).all()
    
    return {category: total for category, total in category_expenses}

def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    """Delete a transaction (only if it belongs to the user)"""
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()
    
    if transaction:
        db.delete(transaction)
        db.commit()
        return True
    return False 