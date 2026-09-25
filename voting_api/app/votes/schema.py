from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class VoteCreate(BaseModel):
    voter_id: int
    candidate_id: int


class VoteResponse(BaseModel):
    id: int
    voter_id: int
    candidate_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateStatistics(BaseModel):
    candidate_id: int
    candidate_name: str
    party: Optional[str]
    votes: int
    percentage: float


class VoteStatisticsResponse(BaseModel):
    total_votes: int
    total_voters_who_voted: int
    results: List[CandidateStatistics]
