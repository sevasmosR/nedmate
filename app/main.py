# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import business, branch, expense

app = FastAPI(title="Business Expense Forecast API")

# CORS setup
origins = ["*"]  # Allow all origins (for testing). Replace with your frontend URL in production.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # List of allowed origins
    allow_credentials=True,      # Allow cookies, authorization headers
    allow_methods=["*"],         # Allow all HTTP methods
    allow_headers=["*"],         # Allow all headers
)

# Include route modules
app.include_router(business.router, prefix="/business", tags=["business"])
app.include_router(branch.router, prefix="/branch", tags=["branch"])
app.include_router(expense.router, prefix="/expense", tags=["expense"])

@app.get("/")
def root():
    return {"message": "Business Expense Forecast API is running"}
