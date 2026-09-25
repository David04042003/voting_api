from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import verify_token
from app.voters import service
from app.voters.schema import VoterCreate, VoterResponse

router = APIRouter(
    prefix="/voters",
    tags=["Voters"],
    dependencies=[Depends(verify_token)]
)


@router.post("/", response_model=VoterResponse, status_code=201)
def create_voter(voter: VoterCreate, db: Session = Depends(get_db)):
    return service.create_voter(db, voter)


@router.get("/", response_model=List[VoterResponse])
def get_voters(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    name: str | None = Query(None, description="Filter voters by name"),
    email: str | None = Query(None, description="Filter voters by email"),
    has_voted: bool | None = Query(None, description="Filter voters by voting status"),
    db: Session = Depends(get_db)
):
    return service.get_voters(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        email=email,
        has_voted=has_voted
    )


@router.get("/{voter_id}", response_model=VoterResponse)
def get_voter_by_id(voter_id: int, db: Session = Depends(get_db)):
    return service.get_voter_by_id(db, voter_id)


@router.delete("/{voter_id}")
def delete_voter(voter_id: int, db: Session = Depends(get_db)):
    return service.delete_voter(db, voter_id)
