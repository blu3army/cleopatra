import datetime
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.base import Base

def default_tomorrow():
    return datetime.date.today() + datetime.timedelta(days=1)

class Cheque(Base):
    __tablename__ = 'cheques'

    id = Column(Integer, primary_key=True)

    number = Column(String(50), nullable=False)

    amount = Column(Numeric(15, 2), nullable=False, default=0)

    payment_date = Column(Date, default=default_tomorrow)

    #issuing_bank_id = Column(Integer, ForeignKey('banks.id'))

    issue_date = Column(Date, default=datetime.date.today)

    direction = Column(String(3), nullable=False)

    party = Column(String(50), nullable=False)

    # __table_args__ = (
    #     UniqueConstraint('company_id', 'number', name='uq_cheques_company_id_number'),
    # )



    def __repr__(self):
        return f'Cheque {self.number}, {self.amount}, {self.payment_date}, {self.issue_date}, {self.direction}, {self.party}'

