from sqlalchemy import Column, Integer, String

from db.base import Base


class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    canonical_name = Column(String, unique=True, nullable=False)
