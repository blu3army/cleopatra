from pdf2image import convert_from_path
from PIL import Image
import io
import base64
from typing import Optional

def pdf_to_base64(path_pdf: str) -> str:
    print("Exec pdf_to_base64")

    try:
        pages = convert_from_path(path_pdf, first_page=1, last_page=1)
    except Exception as e:
        print("❌ ERROR EN convert_from_path:")
        print(e)
        raise


    image = pages[0]

    buffer = io.BytesIO()

    image.save(buffer, format="JPEG")

    b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return b64

