# models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

# --- Business model ---
class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    industry = Column(String, nullable=True)

    branches = relationship("Branch", back_populates="business")


# --- Branch model ---
class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))

    business = relationship("Business", back_populates="branches")
    expenses = relationship("Expense", back_populates="branch")


# --- Expense model ---
class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)

    # Basic info
    merchant = Column(String, index=True, nullable=True)
    category = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    date = Column(Date, nullable=True)
    raw_text = Column(String, nullable=True)

    # Invoice-specific fields
    invoice_id = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    subtotal = Column(Float, nullable=True)
    total_tax = Column(Float, nullable=True)
    previous_unpaid_balance = Column(Float, nullable=True)
    customer_name = Column(String, nullable=True)
    customer_id = Column(String, nullable=True)
    billing_address = Column(String, nullable=True)
    billing_address_recipient = Column(String, nullable=True)
    shipping_address = Column(String, nullable=True)
    service_address = Column(String, nullable=True)
    vendor_address = Column(String, nullable=True)
    vendor_name = Column(String, nullable=True)
    purchase_order = Column(String, nullable=True)
    remittance_address = Column(String, nullable=True)
    service_start_date = Column(Date, nullable=True)
    service_end_date = Column(Date, nullable=True)

    # Line items stored as JSON
    items = Column(JSON, nullable=True)

    # Relationships
    branch_id = Column(Integer, ForeignKey("branches.id"))
    branch = relationship("Branch", back_populates="expenses")
