from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.candidates.model import Candidate
from app.candidates.schema import CandidateCreate
from app.voters.model import Voter
from app.votes.model import Vote


def create_candidate(db: Session, candidate: CandidateCreate):
    existing_voter = db.query(Voter).filter(
        Voter.name.ilike(candidate.name)
    ).first()

    if existing_voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This person is already registered as a voter"
        )

    db_candidate = Candidate(
        name=candidate.name,
        party=candidate.party
    )

    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    return db_candidate


def get_candidates(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    party: str | None = None
):
    query = db.query(Candidate)

    if name:
        query = query.filter(Candidate.name.ilike(f"%{name}%"))

    if party:
        query = query.filter(Candidate.party.ilike(f"%{party}%"))

    return query.order_by(Candidate.id.asc()).offset(skip).limit(limit).all()


def get_candidate_by_id(db: Session, candidate_id: int):
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    return candidate


def delete_candidate(db: Session, candidate_id: int):
    candidate = get_candidate_by_id(db, candidate_id)

    related_votes = db.query(Vote).filter(
        Vote.candidate_id == candidate_id
    ).all()

    for vote in related_votes:
        voter = db.query(Voter).filter(
            Voter.id == vote.voter_id
        ).first()

        if voter:
            voter.has_voted = False

    db.delete(candidate)
    db.commit()

    return {"message": "Candidate deleted successfully"}
