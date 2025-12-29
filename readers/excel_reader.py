import pandas as pd

from readers.column_map import COLUMN_MAP
from readers.detect_bank_by_text import detect_bank_by_text
from readers.normalize_header import normalize_header


def read_cheques_from_excel(path_xlsx: str):
    df = pd.read_excel(path_xlsx)
    # print(df.head())
    # print(df.head())
    # print(df.to_json)

    col_map_real_a_canonico = {}

    for real_col in df.columns:

        norm = normalize_header(real_col)

        if norm in COLUMN_MAP:
            canon = COLUMN_MAP[norm]
            col_map_real_a_canonico[canon] = real_col


    cheques = []

    for i, row in df.iterrows():

        cheque = {
            "cheque_number": str(row.get(col_map_real_a_canonico.get("cheque_number", ""), "")),
            "amount": float(row.get(col_map_real_a_canonico.get("amount", 0), 0)),
            "issue_date": row.get(col_map_real_a_canonico.get("issue_date", ""), None),
            "issuing_bank": detect_bank_by_text(
                row.get(
                    col_map_real_a_canonico.get("issuing_bank", ""),
                None)
            ),
            "payment_date": row.get(col_map_real_a_canonico.get("payment_date", ""), None),
            "drawer": row.get(col_map_real_a_canonico.get("drawer", ""), None),
            "payee": row.get(col_map_real_a_canonico.get("payee", ""), None),
        }
        cheques.append(cheque)

    return cheques


