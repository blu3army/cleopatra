import datetime
import os

from db.base import Base
from db.engine import engine
from db.models.payment import Cheque
from db.services.payment_service import create_payment
from db.session import SessionLocal
from get_pdf_cheques import get_pdf_cheques
from readers.excel_reader import read_cheques_from_excel
from pathlib import Path


def start_app():
    print("CLEOPATRA APP")

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


    # pdfs_list = ["./data/ch4.pdf", "./data/ch3.pdf"]
    pdfs_list = []
    folder_path = "./data/test/22-12-25"

    # for f in os.listdir(folder_path):
    #     full_path = os.path.join('data', 'test', f)
    #     if os.path.isfile(full_path):
    #         pdfs_list.append(full_path)
    #
    #
    # print("Paths ")
    # print(pdfs_list)
    # process_pdf_cheques(pdfs_list=pdfs_list)


    pdf_folder = Path(folder_path)
    pdf_files = list(pdf_folder.glob("*.pdf"))

    for pdf_file in pdf_files:
        pdfs_list.append(pdf_file)
        print(f"File {pdf_file}")

    cheques_list = process_pdf_cheques(pdfs_list=pdfs_list)

    sum = 0
    for cheque in cheques_list:
        sum += cheque.get("amount")

    print(f"Sum of cheques: {sum}")




def process_pdf_cheques(pdfs_list) -> list:

    cheques_list = []

    for path in pdfs_list:
        try:
            data = get_pdf_cheques(path_pdf=path)
            cheques_list.append(data.get("cheques")[0])
            print(f"{path} is done")
        except Exception as e:
            print(f"{path} is not done")

    return cheques_list

def process_excel_cheques(path_excel):
    db = SessionLocal()

    cheques_list = read_cheques_from_excel(path_excel)

    # Bulk insert

    # db.bulk_insert_mappings(Cheque, cheques)
    # db.commit()

    # Simple insert con for
    for cheque in cheques_list:
        try:
            cheque = create_payment(db, data=cheque)

            print(f"Cheque saved: {cheque.number}")

        except Exception as e:
            db.rollback()
            print(f"Error saving cheque {e}")

def create_simple_cheque(db):
    try:
        cheque = create_payment(db, data={
            "number": "32225180",
            "amount": 1500000,
            "drawer": "Karabin Elizabeth",
            "payee": "Agroazul SRL",
            "issuing_bank": "Banco Macro",
            "issue_date": datetime.date(2025, 12, 1),
            "payment_date": datetime.date(2026, 2, 15),
        })

        print(f"Cheque saved: {cheque.number}")

    except Exception as e:
        print(f"Error saving cheque {e}")


if __name__ == "__main__":
    start_app()
