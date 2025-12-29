from readers.detect_bank_by_text import detect_bank_by_text
from readers.detect_bank_by_vision import detect_bank_by_vision
from readers.pdf_reader import pdf_to_text
from extractors.cheque_extractor import extract_cheques_from_text

def get_pdf_cheques(path_pdf: str):
    text = pdf_to_text(path_pdf)

    issuing_bank = detect_bank_by_text(text)

    data = extract_cheques_from_text(text)

    if issuing_bank is None:
        issuing_bank = detect_bank_by_vision(path_pdf)

    if issuing_bank is not None:
        for cheque in data.get("cheques", []):
            # solo si tu schema tiene este campo:
            cheque["issuing_bank"] = issuing_bank



    print(data)
    return data