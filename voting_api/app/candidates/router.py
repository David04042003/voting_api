from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import verify_token
from app.candidates import service
from app.candidates.schema import CandidateCreate, CandidateResponse

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"],
    dependencies=[Depends(verify_token)]
)


@router.post("/", response_model=CandidateResponse, status_code=201)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    return service.create_candidate(db, candidate)


@router.get("/", response_model=List[CandidateResponse])
def get_candidates(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    name: str | None = Query(None, description="Filter candidates by name"),
    party: str | None = Query(None, description="Filter candidates by political party"),
    db: Session = Depends(get_db)
):
    return service.get_candidates(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        party=party
    )


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate_by_id(candidate_id: int, db: Session = Depends(get_db)):
    return service.get_candidate_by_id(db, candidate_id)


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    return service.delete_candidate(db, candidate_id)
