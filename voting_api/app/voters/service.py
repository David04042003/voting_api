from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.voters.model import Voter
from app.voters.schema import VoterCreate
from app.candidates.model import Candidate
from app.votes.model import Vote


def create_voter(db: Session, voter: VoterCreate):
    existing_voter = db.query(Voter).filter(
        Voter.email == voter.email
    ).first()

    if existing_voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    existing_candidate = db.query(Candidate).filter(
        Candidate.name.ilike(voter.name)
    ).first()

    if existing_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This person is already registered as a candidate"
        )

    db_voter = Voter(
        name=voter.name,
        email=voter.email
    )

    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)

    return db_voter


def get_voters(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    email: str | None = None,
    has_voted: bool | None = None
):
    query = db.query(Voter)

    if name:
        query = query.filter(Voter.name.ilike(f"%{name}%"))

    if email:
        query = query.filter(Voter.email.ilike(f"%{email}%"))

    if has_voted is not None:
        query = query.filter(Voter.has_voted == has_voted)

    return query.order_by(Voter.id.asc()).offset(skip).limit(limit).all()


def get_voter_by_id(db: Session, voter_id: int):
    voter = db.query(Voter).filter(
        Voter.id == voter_id
    ).first()

    if not voter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voter not found"
        )

    return voter


def delete_voter(db: Session, voter_id: int):
    voter = get_voter_by_id(db, voter_id)

    existing_vote = db.query(Vote).filter(
        Vote.voter_id == voter_id
    ).first()

    if existing_vote:
        candidate = db.query(Candidate).filter(
            Candidate.id == existing_vote.candidate_id
        ).first()

        if candidate and candidate.votes > 0:
            candidate.votes -= 1

    db.delete(voter)
    db.commit()

    return {"message": "Voter deleted successfully"}
