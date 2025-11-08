# routes/business.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Business, Branch
from app.ocr import parse_invoice


import pandas as pd

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{business_id}/summary")
def business_summary(business_id: int):
    db = next(get_db())
    business = db.query(models.Business).filter(models.Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    # Aggregate expenses across all branches
    expenses = []
    for branch in business.branches:
        for exp in branch.expenses:
            expenses.append({"branch": branch.name, "date": exp.date, "amount": exp.amount})

    if not expenses:
        return {"total": 0, "by_branch": [], "monthly": []}

    df = pd.DataFrame(expenses)
    total = df["amount"].sum()
    by_branch = df.groupby("branch")["amount"].sum().reset_index().to_dict(orient="records")
    monthly = df.groupby(pd.to_datetime(df["date"]).dt.to_period("M"))["amount"].sum().reset_index().to_dict(orient="records")

    return {"business_id": business_id, "total": total, "by_branch": by_branch, "monthly": monthly}
