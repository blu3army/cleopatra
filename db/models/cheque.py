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

    company_id = Column(Integer, ForeignKey('companies.id'))

    payee_id = Column(Integer, ForeignKey('payees.id'))

    issuing_bank_id = Column(Integer, ForeignKey('banks.id'))

    status = Column(String(50), nullable=False, default='pending')

    issue_date = Column(Date, default=datetime.date.today)

    __table_args__ = (
        UniqueConstraint('company_id', 'number', name='uq_cheques_company_id_number'),
    )




