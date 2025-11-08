# routes/expense.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Business, Branch, Expense
from app.ocr import parse_invoice
from datetime import datetime
import imghdr
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from datetime import datetime, date



router = APIRouter()

ALLOWED_EXTENSIONS = ["pdf", "jpeg", "png", "jpg"]  # supported formats

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def allowed_file(filename: str, contents: bytes):
    # Check extension first
    ext = filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False

    # For images, confirm MIME type matches
    if ext in ["jpeg", "jpg", "png"]:
        img_type = imghdr.what(None, h=contents)
        if img_type != ext:
            return False
    return True

@router.post("/upload/{branch_id}")
async def upload_expense(branch_id: int, file: UploadFile = File(...), category: str = "invoice"):
    db = next(get_db())
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    contents = await file.read()

    if not allowed_file(file.filename, contents):
        raise HTTPException(status_code=400, detail="Unsupported file format. Supported: PDF, PNG, JPG, JPEG")

    try:
        invoice_data = parse_invoice(contents)
        if not invoice_data:
            raise HTTPException(status_code=400, detail="Unable to parse invoice. Check file format or content.")

        # Convert CurrencyValue to float if needed
        total_amount = getattr(invoice_data.get("total"), "amount", 0.0) if invoice_data.get("total") else 0.0

        expense = Expense(
            branch_id=branch.id,
            merchant=invoice_data.get("merchant") or "Unknown",
            category=category,
            amount=total_amount,
            date=invoice_data.get("invoice_date") or datetime.utcnow(),
            raw_text=contents.decode("utf-8", errors="ignore")[:1000]
        )

        db.add(expense)
        db.commit()
        db.refresh(expense)

        return {
            "status": "ok",
            "expense_id": expense.id,
            "branch": branch.name,
            "parsed": invoice_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process invoice: {str(e)}")
    
@router.get("/list")
def list_expenses(
    branch_id: int = Query(None, description="Filter by branch ID"),
    db: Session = Depends(get_db)
):
    query = db.query(Expense)
    if branch_id:
        query = query.filter(Expense.branch_id == branch_id)
    
    expenses = query.order_by(Expense.date.desc()).all()
    results = []
    for e in expenses:
        results.append({
            "id": e.id,
            "branch_id": e.branch_id,
            "merchant": e.merchant,
            "category": e.category,
            "amount": e.amount,
            "date": e.date,
            "raw_text": e.raw_text[:100],
        })
    return {"count": len(results), "expenses": results}

@router.get("/summary")
def get_expense_summary(
    start_date: date = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    query = db.query(Expense)

    # Apply date filters if provided
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    # Total expenses
    total_expenses = query.with_entities(func.sum(Expense.amount)).scalar() or 0.0

    # Group by category
    category_summary = (
        query.with_entities(Expense.category, func.sum(Expense.amount))
        .group_by(Expense.category)
        .all()
    )
    by_category = {cat: amt for cat, amt in category_summary}

    # Group by branch
    branch_summary = (
        query.join(Branch, Expense.branch_id == Branch.id)
        .with_entities(Branch.name, func.sum(Expense.amount))
        .group_by(Branch.name)
        .all()
    )
    by_branch = {name: amt for name, amt in branch_summary}

    return {
        "filters": {"start_date": start_date, "end_date": end_date},
        "total_expenses": total_expenses,
        "by_category": by_category,
        "by_branch": by_branch,
    }
