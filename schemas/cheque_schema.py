cheque_schema = {
    "name": "cheques",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "cheques": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "cheque_number": {"type": "string"},
                        "amount": {"type": "number"},
                        #"drawer": {"type": "string"},
                        "payee": {"type": "string"},
                        "issuing_bank": {"type": ["string", "null"] },
                        "issue_date": {
                            "type": ["string", "null"],
                            "description": "Fecha de emisión en formato YYYY-MM-DD o null",
                        },
                        "payment_date": {
                            "type": ["string", "null"],
                            "description": "Fecha de pago/vencimiento en formato YYYY-MM-DD o null",
                        },
                    },
                    "required": [
                        "cheque_number",
                        "amount",
                        #"drawer",
                        "payee",
                        "issuing_bank",
                        "issue_date",
                        "payment_date",
                    ],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["cheques"],
        "additionalProperties": False,
    },
}
