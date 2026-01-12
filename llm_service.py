from mistralai import Mistral
from config import MODEL_LLM

def summarize_text(api_key: str, text: str) -> str:
    client = Mistral(api_key=api_key)
    res = client.chat.complete(
        model=MODEL_LLM,
        messages=[
            {"role": "system", "content": "Summarize the document"},
            {"role": "user", "content": text}
        ]
    )
    return res.choices[0].message.content

def qa_text(api_key: str, text: str, question: str) -> str:
    client = Mistral(api_key=api_key)
    res = client.chat.complete(
        model=MODEL_LLM,
        messages=[
            {"role": "system", "content": "Answer only from the document"},
            {"role": "user", "content": f"Text:\n{text}\n\nQuestion:\n{question}"}
        ]
    )
    return res.choices[0].message.content
