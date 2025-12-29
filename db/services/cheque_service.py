from sqlalchemy.orm import Session
from db.models.cheque import Cheque


def create_cheque(db: Session, data: dict) -> Cheque:

    print("\nData for create cheque")
    print(data)

    # Antes de crear el cheque, debemos obtener la
    # company_id
    # payee_id


    new_cheque = Cheque(
        number=data.get("cheque_number"),
        amount=data.get("amount"),
        drawer=data.get("drawer"),
        payee=data.get("payee"),
        issuing_bank=data.get("issuing_bank"),
        issue_date=data.get("issue_date"),
        payment_date=data.get("payment_date"),
    )

    db.add(new_cheque)
    db.commit()
    db.refresh(new_cheque)

    return new_cheque