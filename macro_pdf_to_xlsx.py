import os
import re
from datetime import datetime
from typing import List, Dict, Optional

import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageOps

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

from pathlib import Path
# -----------------------------
# CONFIG (adjust paths if needed)
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent

# PDF_PATH = r"C:\ruta\06-EXTRACTO MACRO ABRIL 2025.pdf"
# OUT_XLSX = r"C:\ruta\EXTRACTO_MACRO_ABRIL_2025.xlsx"

PDF_PATH = BASE_DIR / "data" / "estudio" / "06-EXTRACTO MACRO ABRIL 2025.pdf"
OUT_XLSX = BASE_DIR / "data" / "estudio" / "EXTRACTO_MACRO_ABRIL_2025.xlsx"

# If you installed Tesseract in the default location:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# If Poppler is not in PATH, set this:
POPPLER_BIN = r"C:\poppler\Library\bin"  # or None if already in PATH


# -----------------------------
# OCR + Parsing helpers
# -----------------------------
DATE_RE = re.compile(r"^\s*(\d{1,2}/\d{1,2}/\d{2,4})\s+(.*)$")
MONEY_RE = re.compile(r"-?\d{1,3}(?:[.\s]\d{3})*(?:,\d{2})")  # Macro usually uses comma decimals
REF_RE = re.compile(r"\b(\d{3,})\b")

# Try to detect the movement table area and ignore headers/footers
def preprocess_for_ocr(img: Image.Image) -> Image.Image:
    # Crop margins (tuned for typical bank statement layout)
    w, h = img.size
    # You can adjust these if needed:
    left = int(w * 0.03)
    right = int(w * 0.97)
    top = int(h * 0.18)
    bottom = int(h * 0.95)

    img = img.crop((left, top, right, bottom))
    img = ImageOps.grayscale(img)
    # Optional: increase contrast slightly by autocontrast
    img = ImageOps.autocontrast(img)
    return img

DATE_RE = re.compile(r"^\s*(\d{2}/\d{2}/\d{2,4})\s+(.*)$")

# money like 114.649,31 or 9.066.478,73 (sometimes OCR adds spaces)
MONEY_RE = re.compile(r"-?\d{1,3}(?:\.\d{3})*,\d{2}")
INT_RE = re.compile(r"^\d{1,10}$")

FOOTER_PREFIXES = (
    "Los depósitos",
    "El presente extracto",
    "Usted puede",
    "Ley ",
    "B.C.R.A",
)

def parse_ars_money(s: str) -> float:
    s = s.strip().replace(".", "").replace(",", ".")
    return float(s)

def is_footer_line(line: str) -> bool:
    l = line.strip()
    return any(l.startswith(p) for p in FOOTER_PREFIXES)

def infer_is_credit(desc: str) -> bool:
    d = desc.upper()
    credit_markers = ("ACREDITACION", "ACREDITACIÓN", "N/C", "CREDIN", "CCERR")
    debit_markers  = ("N/D", "DB ", "DEBITO", "DÉBITO", "RETENC", "RET.", "PAGO", "COMISION", "IMPUESTO", "IVA")
    if any(m in d for m in credit_markers) and not any(m in d for m in debit_markers):
        return True
    return False

def parse_macro_movements(lines):
    """
    Extract only:
      CUENTA CORRIENTE BANCARIA NRO.: 3-006-0941947724-7
      under DETALLE DE MOVIMIENTO table.
    Output columns:
      Fecha, Descripcion, Referencia, Debitos, Creditos, Saldo
    """

    target_account = "CUENTA CORRIENTE BANCARIA NRO.: 3-006-0941947724-7"
    in_target = False
    in_table = False

    rows = []
    current = None
    prev_saldo = None

    def flush():
        nonlocal current, prev_saldo
        if not current:
            return

        text = " ".join(current["parts"]).strip()

        # Extract money tokens
        m_tokens = MONEY_RE.findall(text)
        if len(m_tokens) < 2:
            current = None
            return

        amts = [parse_ars_money(x) for x in m_tokens]
        saldo = amts[-1]

        # Everything before first money = desc + ref candidates
        first_money = MONEY_RE.search(text)
        before = text[:first_money.start()].strip()

        # reference = last pure integer token before amounts
        tokens = before.split()
        ref = ""
        desc = before
        if tokens and INT_RE.match(tokens[-1]):
            ref = tokens[-1]
            desc = " ".join(tokens[:-1]).strip()

        # Determine debit/credit
        debit = 0.0
        credit = 0.0

        if len(amts) >= 4:
            # sometimes: debitos + creditos + saldo (plus maybe another)
            # safest: take the last 3 numeric columns before saldo as deb/cred, but this is rare
            debit = abs(amts[-3])
            credit = abs(amts[-2])
        elif len(amts) == 3:
            # common: ref(0) + amount + saldo  OR  amount + saldo + (noise)
            movement = abs(amts[-2])
            if prev_saldo is not None:
                delta = saldo - prev_saldo
                if delta >= 0:
                    credit = movement
                else:
                    debit = movement
            else:
                credit = movement if infer_is_credit(desc) else 0.0
                debit = movement if not infer_is_credit(desc) else 0.0
        else:
            # len == 2: amount + saldo
            movement = abs(amts[-2])
            if prev_saldo is not None:
                delta = saldo - prev_saldo
                if delta >= 0:
                    credit = movement
                else:
                    debit = movement
            else:
                credit = movement if infer_is_credit(desc) else 0.0
                debit = movement if not infer_is_credit(desc) else 0.0

        rows.append({
            "Fecha": current["fecha"],
            "Descripcion": desc,
            "Referencia": ref,
            "Debitos": float(debit),
            "Creditos": float(credit),
            "Saldo": float(saldo),
        })

        prev_saldo = saldo
        current = None

    for line in lines:
        line_stripped = line.strip()

        # enter target account section
        if target_account in line_stripped:
            in_target = True
            in_table = False
            current = None
            prev_saldo = None
            continue

        if not in_target:
            continue

        # stop if another account starts (optional extra safety)
        if line_stripped.startswith("CUENTA CORRIENTE") and target_account not in line_stripped and "BANCARIA" in line_stripped:
            flush()
            break

        # table start
        if line_stripped == "DETALLE DE MOVIMIENTO":
            continue

        if line_stripped == "FECHA DESCRIPCION REFERENCIA DEBITOS CREDITOS SALDO":
            in_table = True
            continue

        if not in_table:
            continue

        # ignore saldo lines and footers
        u = line_stripped.upper()
        if u.startswith("SALDO ULTIMO EXTRACTO") or u.startswith("SALDO FINAL") or u.startswith("TOTAL COBRADO"):
            continue
        if is_footer_line(line_stripped):
            flush()
            break

        m = DATE_RE.match(line_stripped)
        if m:
            flush()
            date_str, rest = m.group(1), m.group(2)

            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError:
                dt = datetime.strptime(date_str, "%d/%m/%y").date()

            current = {"fecha": dt, "parts": [rest]}
        else:
            if current:
                # continuation of description
                current["parts"].append(line_stripped)

    flush()
    return rows

def extract_desc_and_ref(before_amount: str) -> (str, str):
    # Reference rule (Macro style): last numeric token before amounts
    parts = before_amount.split()
    ref = ""
    desc = before_amount.strip()
    if parts and re.fullmatch(r"\d{3,}", parts[-1]):
        ref = parts[-1]
        desc = " ".join(parts[:-1]).strip()
    return desc, ref

def write_xlsx(rows: List[Dict], out_path: str) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Extracto"

    headers = ["Fecha", "Descripcion", "Referencia", "Debitos", "Creditos", "Saldo"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(vertical="center")

    for r in rows:
        ws.append([
            r["Fecha"],
            r["Descripcion"],
            r["Referencia"],
            r["Debitos"],
            r["Creditos"],
            r["Saldo"],
        ])

    col_idx = {name: i + 1 for i, name in enumerate(headers)}
    # Formats
    for row_i in range(2, ws.max_row + 1):
        ws.cell(row=row_i, column=col_idx["Fecha"]).number_format = "yyyy-mm-dd"
        ws.cell(row=row_i, column=col_idx["Fecha"]).alignment = Alignment(vertical="top")

        ws.cell(row=row_i, column=col_idx["Descripcion"]).alignment = Alignment(wrap_text=True, vertical="top")

        for c in ["Debitos", "Creditos", "Saldo"]:
            ws.cell(row=row_i, column=col_idx[c]).number_format = "#,##0.00"
            ws.cell(row=row_i, column=col_idx[c]).alignment = Alignment(vertical="top")

    widths = {"Fecha": 12, "Descripcion": 70, "Referencia": 16, "Debitos": 14, "Creditos": 14, "Saldo": 14}
    for name, w in widths.items():
        ws.column_dimensions[get_column_letter(col_idx[name])].width = w

    ws.freeze_panes = "A2"
    wb.save(out_path)

def ocr_pdf_to_lines(pdf_path: str) -> List[str]:
    images = convert_from_path(
        pdf_path,
        dpi=200,
        poppler_path=POPPLER_BIN if POPPLER_BIN else None
    )

    lines: List[str] = []
    for img in images:
        img2 = preprocess_for_ocr(img)
        text = pytesseract.image_to_string(img2, lang="spa", config="--oem 1 --psm 6")
        for ln in text.splitlines():
            ln = ln.strip()
            if ln:
                lines.append(ln)
    return lines

def debug_save_cropped_page(pdf_path: str, page_index: int = 0):
    images = convert_from_path(pdf_path, dpi=250, poppler_path=POPPLER_BIN if POPPLER_BIN else None)
    img = preprocess_for_ocr(images[page_index])
    out = Path(__file__).resolve().parent / f"debug_crop_page_{page_index+1}.png"
    img.save(out)
    print(f"[DEBUG] Saved cropped page image: {out}")


def debug_dump_ocr_lines(pdf_path: str, max_pages: int = 2):
    images = convert_from_path(pdf_path, dpi=250, poppler_path=POPPLER_BIN if POPPLER_BIN else None)
    lines = []
    for i, img in enumerate(images[:max_pages]):
        img2 = preprocess_for_ocr(img)
        text = pytesseract.image_to_string(img2, lang="spa", config="--oem 1 --psm 6")
        for ln in text.splitlines():
            ln = ln.strip()
            if ln:
                lines.append(f"[P{i+1}] {ln}")

    out = os.path.join(os.path.dirname(__file__), "debug_ocr.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[DEBUG] OCR saved to: {out}")

    # Show likely movement lines (dates)
    date_like = re.compile(r"\b\d{1,2}[/-]\d{1,2}\b")
    hits = [ln for ln in lines if date_like.search(ln)]
    print(f"[DEBUG] Lines with date-like patterns found: {len(hits)}")
    print("\n".join(hits[:30]))


def main():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    print("OCR... (this may take a few minutes for long PDFs)")
    lines = ocr_pdf_to_lines(PDF_PATH)

    print("Parsing movements...")
    rows = parse_macro_movements(lines)

    if not rows:
        raise RuntimeError("No movements were parsed. You may need to adjust cropping or patterns.")

    print(f"Writing Excel: {OUT_XLSX}")
    write_xlsx(rows, OUT_XLSX)
    print("Done.")

if __name__ == "__main__":
    main()
