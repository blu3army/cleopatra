from readers.detect_bank_by_text import detect_bank_by_text
from readers.detect_bank_by_vision import detect_bank_by_vision
from readers.excel_reader import read_cheques_from_excel
from readers.pdf_reader import pdf_to_text
from extractors.cheque_extractor import extract_cheques_from_text
from readers.read_cheque_by_vision import read_cheque_by_vision, read_pdf_page_by_vision, parse_cheques_with_openai


def get_pdf_cheques(path_pdf: str):

    # We try to get data from pdf with pdf lector
    text = pdf_to_text(path_pdf)

    data = None
    issuing_bank = None

    # In case we cannot get data by lector, we need to read by vision
    if not text or not text.strip():
        print("No text found")

        text = read_pdf_page_by_vision(path_pdf)

        print(f"Read {text} pages")

        #response = parse_cheques_with_openai(text)

        #print(f"\n\nCheque response: {response}")

    else:
        data = extract_cheques_from_text(text)
        issuing_bank = detect_bank_by_text(text)




    if issuing_bank is None:
        issuing_bank = detect_bank_by_vision(path_pdf)

    if issuing_bank is not None:
        for cheque in data.get("cheques", []):
            # solo si tu schema tiene este campo:
            cheque["issuing_bank"] = issuing_bank



    print(data)
    return data