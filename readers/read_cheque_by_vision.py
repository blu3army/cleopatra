import json

import numpy as np
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from openai import OpenAI
import cv2

from schemas.cheque_schema import cheque_schema

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

client = OpenAI()

def read_cheque_by_vision(path_pdf: str) -> str:

    images = convert_from_path(path_pdf, dpi=300)

    text = ""

    for img in images:
        text += pytesseract.image_to_string(img, lang="spa")

    return text


def preprocess(img: Image.Image) -> Image.Image:
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return Image.fromarray(gray)


def read_pdf_page_by_vision(path_pdf: str) -> str:
    images = convert_from_path(path_pdf, dpi=300, first_page=1, last_page=1)

    img = images[0]

    img = preprocess(img)

    text = pytesseract.image_to_string(img, lang="spa", config="--psm 4")

    return text




def parse_cheques_with_openai(cheques_text: str) -> list[dict]:

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un sistema contable especializado en cheques bancarios. "
                    "En el texto puede haber uno o varios cheques. "
                    "Extrae todos los cheques encontrados."
                )
            },
            {
                "role": "user",
                "content": (
                    "Extrae todos los cheques bancarios del siguiente texto OCR:\n\n"
                    f"{cheques_text}"
                )
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": cheque_schema,
        },
    )

    content = response.choices[0].message.content
    data = json.loads(content)

    return data["cheques"]

