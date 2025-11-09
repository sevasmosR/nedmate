from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import transactions  # import your new router

app = FastAPI(title="NedMate AI API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(transactions.router, prefix="/api", tags=["transactions"])
