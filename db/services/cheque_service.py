from datetime import date

from sqlalchemy.orm import Session
from db.models.cheque import Cheque


def create_cheque(db: Session, data: dict) -> Cheque:

    print("\nData for create cheque")
    print(data)

    # Antes de crear el cheque, debemos obtener:
    # party_id


    new_cheque = Cheque(
        number=data.get("number"),
        amount=data.get("amount"),
        party=data.get("party"),
        issue_date=date.today(),
        payment_date=data.get("due"),
        direction=data.get("dir")
    )

    db.add(new_cheque)
    db.commit()
    db.refresh(new_cheque)

    return new_cheque

def get_cheques(db: Session, filters) -> list[Cheque]:

    query = db.query(Cheque)

    if filters.get("dir"):
        query = query.filter(Cheque.direction == filters.get("dir"))

    if filters.get("party"):
        query = query.filter(Cheque.party == filters.get("party"))

    if filters.get("since"):
        query = query.filter(Cheque.payment_date >= filters.get("since"))

    if filters.get("until"):
        query = query.filter(Cheque.payment_date <= filters.get("until"))

    if filters.get("max_amount"):
        query = query.filter(Cheque.amount <= filters.get("max_amount"))

    if filters.get("min_amount"):
        query = query.filter(Cheque.amount >= filters.get("min_amount"))

    cheques = query.all()

    return cheques
