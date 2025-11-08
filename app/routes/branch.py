# routes/branch.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Business, Branch
from app.ocr import parse_invoice

import pandas as pd

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{branch_id}/summary")
def branch_summary(branch_id: int):
    db = next(get_db())
    branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    expenses = [{"date": e.date, "amount": e.amount} for e in branch.expenses]
    if not expenses:
        return {"total": 0, "monthly": []}

    df = pd.DataFrame(expenses)
    total = df["amount"].sum()
    monthly = df.groupby(pd.to_datetime(df["date"]).dt.to_period("M"))["amount"].sum().reset_index().to_dict(orient="records")

    return {"branch_id": branch_id, "total": total, "monthly": monthly}
