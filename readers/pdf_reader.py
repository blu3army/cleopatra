import pdfplumber

def pdf_to_text(path_pdf: str) -> str:
    """Return all the pdf text concatenated"""

    text = ""

    with pdfplumber.open(path_pdf) as pdf:
        for page in pdf.pages:
            text += ( page.extract_text() or "" ) + "\n"

    return text


