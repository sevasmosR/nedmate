# seed_db.py
from datetime import date
from app.database import SessionLocal
from app.models import Business, Branch, Expense

db = SessionLocal()

# --- Create a Business ---
business = Business(name="Acme Corp", industry="Technology")
db.add(business)
db.commit()
db.refresh(business)

# --- Create Branches ---
branch1 = Branch(name="Main Branch", city="New York", business_id=business.id)
branch2 = Branch(name="West Branch", city="San Francisco", business_id=business.id)
db.add_all([branch1, branch2])
db.commit()
db.refresh(branch1)
db.refresh(branch2)

# --- Create some Expenses ---
expense1 = Expense(
    branch_id=branch1.id,
    merchant="Office Supplies Inc",
    category="office",
    amount=123.45,
    date=date(2023, 1, 15),
    raw_text="Sample invoice text for Office Supplies"
)

expense2 = Expense(
    branch_id=branch2.id,
    merchant="Tech Gadgets Ltd",
    category="electronics",
    amount=987.65,
    date=date(2023, 3, 10),
    raw_text="Sample invoice text for Tech Gadgets"
)

db.add_all([expense1, expense2])
db.commit()

print("Seed data inserted successfully!")
db.close()
