from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import verify_token
from app.votes import service
from app.votes.schema import VoteCreate, VoteResponse, VoteStatisticsResponse

router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
    dependencies=[Depends(verify_token)]
)


@router.post("/", response_model=VoteResponse, status_code=201)
def create_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    return service.create_vote(db, vote)


@router.get("/", response_model=List[VoteResponse])
def get_votes(db: Session = Depends(get_db)):
    return service.get_votes(db)


@router.get("/statistics", response_model=VoteStatisticsResponse)
def get_vote_statistics(db: Session = Depends(get_db)):
    return service.get_vote_statistics(db)
