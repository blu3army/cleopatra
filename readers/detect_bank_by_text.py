from typing import Optional
from readers.normalize_header import normalize_header


def detect_bank_by_text(text) -> Optional[str]:

    t = normalize_header(text)

    bank_patterns = {
        # key que buscamos en el texto   -> nombre estandarizado
        "banco de la nacion argentina": "Banco de la Nación Argentina",
        "banco nacion": "Banco de la Nación Argentina",
        "banco nacin": "Banco de la Nación Argentina",  # por si OCR come la o

        "banco galicia": "Banco Galicia",
        "galicia": "Banco Galicia",

        "banco santander rio": "Banco Santander Río",
        "banco santander": "Banco Santander",
        "santander rio": "Banco Santander Río",
        "santander": "Banco Santander",

        "bbva frances": "BBVA",
        "bbva": "BBVA",

        "banco macro": "Banco Macro",
        "macro": "Banco Macro",

        "banco ciudad": "Banco Ciudad",
        "banco supervielle": "Banco Supervielle",
        "supervielle": "Banco Supervielle",

        "banco corrientes": "Banco Corrientes",
        "banco": "Banco Corrientes",
        "el banco de corrientes": "Banco de Corrientes",

        "hsbc": "HSBC",
        "icbc": "ICBC",
        "banco patagonia": "Banco Patagonia",
        "banco provincia": "Banco Provincia de Buenos Aires",
        "provincia": "Banco Provincia de Buenos Aires",
    }

    for patron, bank_name in bank_patterns.items():
        if patron in t:
            return bank_name

    return None