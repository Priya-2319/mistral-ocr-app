import base64
import json
from docx import Document
from langdetect import detect

def encode_file(file_bytes, mime):
    return f"data:{mime};base64,{base64.b64encode(file_bytes).decode()}"

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"

def download_link(content, filename, mime):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:{mime};base64,{b64}" download="{filename}">⬇️ {filename}</a>'

def export_docx(text, path):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(path)
    
def is_pdf(url: str) -> bool:
    return url.lower().endswith(".pdf")

LANGUAGE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh-cn": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu"
}
