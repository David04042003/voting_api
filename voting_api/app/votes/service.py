from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.votes.model import Vote
from app.votes.schema import VoteCreate
from app.voters.model import Voter
from app.candidates.model import Candidate
from app.voters.service import get_voter_by_id
from app.candidates.service import get_candidate_by_id


def create_vote(db: Session, vote: VoteCreate):
    voter = get_voter_by_id(db, vote.voter_id)
    candidate = get_candidate_by_id(db, vote.candidate_id)

    if voter.has_voted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This voter has already voted"
        )

    db_vote = Vote(
        voter_id=vote.voter_id,
        candidate_id=vote.candidate_id
    )

    try:
        voter.has_voted = True
        candidate.votes += 1

        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)

        return db_vote

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This voter has already voted"
        )


def get_votes(db: Session):
    return db.query(Vote).order_by(Vote.id.asc()).all()


def get_vote_statistics(db: Session):
    total_votes = db.query(Vote).count()

    total_voters_who_voted = db.query(Voter).filter(
        Voter.has_voted == True
    ).count()

    candidates = db.query(Candidate).order_by(
        Candidate.votes.desc(),
        Candidate.id.asc()
    ).all()

    results = []

    for candidate in candidates:
        percentage = 0

        if total_votes > 0:
            percentage = round((candidate.votes / total_votes) * 100, 2)

        results.append({
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
            "party": candidate.party,
            "votes": candidate.votes,
            "percentage": percentage
        })

    return {
        "total_votes": total_votes,
        "total_voters_who_voted": total_voters_who_voted,
        "results": results
    }
