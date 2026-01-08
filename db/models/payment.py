import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.base import Base
from decimal import Decimal

def default_tomorrow():
    return datetime.date.today() + datetime.timedelta(days=1)


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)

    # 1
    direction: Mapped[str] = mapped_column(String(3)) # ["in", "out"]
    # 2
    instrument_type: Mapped[str] = mapped_column(String(50))
    # 3
    reference: Mapped[str] = mapped_column(String(50))
    # 4
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0.00)
    # 5
    payment_date: Mapped[datetime.date] = mapped_column(Date, default=default_tomorrow)
    # 6
    issue_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    # 7
    party: Mapped[str] = mapped_column(String(50), nullable=False)
    # 8
    status: Mapped[str] = mapped_column(String(50), default="pending")

    # __table_args__ = (
    #     UniqueConstraint('company_id', 'number', name='uq_cheques_company_id_number'),
    # )



    def __repr__(self):
        return f'Payment {self.reference} {self.payment_date} {self.payment_date} {self.status} {self.party} {self.direction}'




# id
#
# direction (IN / OUT)
#
# instrument_type
#
# amount
#
# due_date
#
# party_id
#
# status
#
# PENDING → existe pero no venció
#
# DUE → venció hoy o antes y no se ejecutó
#
# SETTLED → se pagó / cobró
#
# REJECTED → rechazado
#
# CANCELLED → anulado
#
# expected_execution_date (normalmente = due_date)
#
# settled_at (nullable)
#
# settled_amount (nullable)
#
# settlement_ref (nullable)
#
# metadata (jsonb)