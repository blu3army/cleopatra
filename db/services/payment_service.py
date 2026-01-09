from datetime import date

from sqlalchemy import delete
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


def delete_payment(db: Session, id: int) -> type[Payment] | None:

    if id:
        payment = db.get(Payment, id)

        if payment.status != "PENDING":
            return None

        if payment:
            db.delete(payment)
            db.commit()

            return payment

    return None

