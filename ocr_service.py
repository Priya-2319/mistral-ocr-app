from mistralai import Mistral
from config import MODEL_OCR

def run_ocr(api_key: str, document: dict) -> str:
    client = Mistral(api_key=api_key)
    response = client.ocr.process(
        model=MODEL_OCR,
        document=document,
        include_image_base64=True
    )
    pages = getattr(response, "pages", [])
    return "\n\n".join(p.markdown for p in pages) or "No text detected"