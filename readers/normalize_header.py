import unicodedata

def normalize_header(name: str) -> str:
    if not isinstance(name, str):
        return ""

    # pasar a minus
    name = name.strip().lower()

    # sacar tildes
    name = "".join(
        c for c in unicodedata.normalize("NFD", name)
        if unicodedata.category(c) != "Mn"
    )

    # reemplazar dobles espacios por uno
    while "  " in name:
        name = name.replace("  ", " ")

    return name
