from sqlalchemy.orm import Session

from db.models.payment import Payment


def list_payments(db: Session, filters) -> list[type[Payment]]:
    print(f"Listing Payments {filters}")

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
