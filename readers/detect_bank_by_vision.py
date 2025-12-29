from openai import OpenAI
from typing import Optional

from readers.pdf_to_base64 import pdf_to_base64

client = OpenAI()

def detect_bank_by_vision(path_pdf: str) -> Optional[str]:

    b64_image = pdf_to_base64(path_pdf)

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Sos un asistente que identifica el banco emisor de un cheque "
                    "a partir de una imagen. Devolvé solo el nombre del banco, nada más."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}",
                        }
                    }
                ]

            }
        ],
        max_tokens=20,
    )
    b64_image = pdf_to_base64(path_pdf)


    bank = resp.choices[0].message.content.strip()

    if bank.lower() == "null":
        return None

    return bank

