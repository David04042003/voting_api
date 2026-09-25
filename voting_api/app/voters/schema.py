from pydantic import BaseModel, EmailStr, ConfigDict, Field


class VoterBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class VoterCreate(VoterBase):
    pass


class VoterResponse(VoterBase):
    id: int
    has_voted: bool

    model_config = ConfigDict(from_attributes=True)
