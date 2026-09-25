from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CandidateBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    party: Optional[str] = Field(default=None, max_length=100)


class CandidateCreate(CandidateBase):
    pass


class CandidateResponse(CandidateBase):
    id: int
    votes: int

    model_config = ConfigDict(from_attributes=True)
