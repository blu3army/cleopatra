from openai import OpenAI
import json
from schemas.cheque_schema import cheque_schema

client = OpenAI()

def extract_cheques_from_text(text: str) -> dict:

    resp = client.chat.completions.create(
        model = "gpt-4.1-mini",
        response_format={
            "type": "json_schema",
            "json_schema": cheque_schema
        },
        messages=[
            {
                "role": "system",
                "content": (
                    "Sos un extractor de datos de cheques. "
                    "Devolvés SOLO un JSON válido según el schema definido."
                    "Si no existe un cheque number explícito, pero sí un transaction number, "
                    "Ignorá el campo CUIT"
                    "entonces usar el transaction number como cheque_number."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Extraé todos los cheques que encuentres en el siguiente texto. "
                    "Si alguna fecha no aparece, poné null.\n\n"
                    f"{text}"
                )
            }
        ]
    )

    raw = resp.choices[0].message.content

    if isinstance(raw, list):
        # concateno todos los fragmentos de texto
        raw = "".join(part.get("text", "") for part in raw if isinstance(part, dict))

    return json.loads(raw)
