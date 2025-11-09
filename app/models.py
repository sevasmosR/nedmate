# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    account = Column(String)
    description = Column(String)
    debit_fc = Column(Float)
    credit_fc = Column(Float)
    balance_fc = Column(Float)
    debit_zar = Column(Float)
    credit_zar = Column(Float)
    balance_zar = Column(Float)
    category = Column(String)
    reference = Column(String)
    currency = Column(String)
    fx_to_zar_at_txn = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    counterparty = Column(String)
