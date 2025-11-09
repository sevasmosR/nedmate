# routes/transactions.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Transaction

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/transactions")
def list_transactions(
    limit: int = Query(100, description="Number of records to return"),
    offset: int = Query(0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    records = db.query(Transaction).order_by(Transaction.date.desc()).offset(offset).limit(limit).all()
    results = []
    for t in records:
        results.append({
            "id": t.id,
            "date": t.date,
            "account": t.account,
            "description": t.description,
            "debit_fc": t.debit_fc,
            "credit_fc": t.credit_fc,
            "balance_fc": t.balance_fc,
            "debit_zar": t.debit_zar,
            "credit_zar": t.credit_zar,
            "balance_zar": t.balance_zar,
            "category": t.category,
            "reference": t.reference,
            "currency": t.currency,
            "fx_to_zar_at_txn": t.fx_to_zar_at_txn,
            "latitude": t.latitude,
            "longitude": t.longitude,
            "counterparty": t.counterparty
        })
    return {"count": len(results), "transactions": results}
