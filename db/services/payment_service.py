from datetime import date

from sqlalchemy import delete
from sqlalchemy.orm import Session
from db.models.payment import Payment


def create_payment(db: Session, data: dict) -> Payment:

    print("\nData for create cheque")
    print(data)


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



def update_payment(
        db: Session, payment_id: int, *,
        ref: str = None,
        amount: float = None,
        due: str = None,
        status: str = None
) -> type[Payment]:

    if all([v is None for v in [amount, due, status, ref]]):
        raise Exception("All fields are None")

    payment = db.get(Payment, payment_id)

    if payment is None:
        raise Exception("Payment with id {} not found".format(payment_id))

    if payment.status != "PENDING":
        raise Exception("Payment with id {} not PENDING".format(payment_id))

    if ref is not None:
        payment.reference = ref

    if amount is not None:
        payment.amount = amount

    if due is not None:
        payment.payment_date = due

    if status is not None:
        payment.status = status

    db.commit()
    db.refresh(payment)

    return payment


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

