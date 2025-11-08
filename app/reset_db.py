# reset_db.py
from app.database import Base, engine

# Import all models so they are registered with SQLAlchemy
from app.models import Business, Branch, Expense

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("Database reset complete!")
