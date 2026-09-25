from fastapi import FastAPI

from app.database import Base, engine

from app.auth.router import router as auth_router
from app.voters.router import router as voters_router
from app.candidates.router import router as candidates_router
from app.votes.router import router as votes_router

from app.voters.model import Voter
from app.candidates.model import Candidate
from app.votes.model import Vote

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Voting API",
    description="REST API for managing voters, candidates and votes.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Voting API is running"}


app.include_router(auth_router)
app.include_router(voters_router)
app.include_router(candidates_router)
app.include_router(votes_router)
