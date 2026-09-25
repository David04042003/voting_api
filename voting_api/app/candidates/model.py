from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    party = Column(String(100), nullable=True)
    votes = Column(Integer, default=0, nullable=False)

    votes_relation = relationship(
        "Vote",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )
