# init_db.py
from .database import Base, engine
from . import models  # register models

def init():
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")

if __name__ == "__main__":
    init()
