from db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum


class Party(Base):
    __tablename__ = "parties"
    id = Column(Integer, primary_key=True)
    cuit = Column(String, unique=True, nullable=False)

    canonical_name = Column(String, nullable=False)
    display_name = Column(String, nullable=False)

    party_type = Column(
        Enum("PERSON", "COMPANY", name="party_type"),
        null=False,
    )