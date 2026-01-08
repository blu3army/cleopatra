from datetime import date

from sqlalchemy.orm import Session
from db.models.payment import Payment


def create_payment(db: Session, data: dict) -> Payment:

    print("\nData for create cheque")
    print(data)

    # Antes de crear el cheque, debemos obtener:
    # party_id


    new_payment = Payment(
        reference=data.get("ref"),
        amount=data.get("amount"),
        party=data.get("party"),
        issue_date=date.today(),
        payment_date=data.get("due"),
        direction=data.get("dir"),
        instrument_type=data.get("type"),
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment

def get_payments(db: Session, filters) -> list[Payment]:

    query = db.query(Payment)

    if filters.get("dir"):
        query = query.filter(Payment.direction == filters.get("dir"))

    if filters.get("party"):
        query = query.filter(Payment.party == filters.get("party"))

    if filters.get("since"):
        query = query.filter(Payment.payment_date >= filters.get("since"))

    if filters.get("until"):
        query = query.filter(Payment.payment_date <= filters.get("until"))

    if filters.get("max_amount"):
        query = query.filter(Payment.amount <= filters.get("max_amount"))

    if filters.get("min_amount"):
        query = query.filter(Payment.amount >= filters.get("min_amount"))

    payments = query.all()

    return payments
