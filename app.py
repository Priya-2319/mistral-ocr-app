import streamlit as st
import json, time
from ocr_service import run_ocr
from llm_service import summarize_text, qa_text
from utils import encode_file, detect_language, download_link, is_pdf
from config import SUPPORTED_FILES

st.set_page_config("Mistral OCR Pro", "🤖", layout="wide")
st.title("🤖 Mistral OCR – Pro Edition")

st.markdown("<h3 style color: white;'>Built by <a href='https://github.com/Priya-2319'>Priya Jha with ❤️ </a></h3>", unsafe_allow_html=True)
with st.expander("Expand Me"):
    st.markdown("""
    This application allows you to extract information from pdf/image based on Mistral OCR.
    """)

# ================= API KEY =================
api_key = st.text_input("🔑 Mistral API Key", type="password")
if not api_key:
    st.stop()

# ================= INPUT TYPE =================
input_type = st.radio("Select input type", ["Upload Files", "URLs"])

uploaded_files = []
urls = []

if input_type == "Upload Files":
    uploaded_files = st.file_uploader(
        "Upload PDFs or Images",
        type=SUPPORTED_FILES,
        accept_multiple_files=True
    )
else:
    urls = st.text_area(
        "Enter PDF/Image URLs (one per line)",
        placeholder="https://example.com/file.pdf\nhttps://example.com/image.png"
    ).splitlines()

# ================= SESSION =================
if "results" not in st.session_state:
    st.session_state.results = []

# ================= RUN OCR =================
if st.button("🚀 Run OCR"):
    st.session_state.results.clear()
    sources = uploaded_files if input_type == "Upload Files" else urls

    if not sources:
        st.warning("No input provided")
        st.stop()

    progress = st.progress(0)

    for i, src in enumerate(sources):

        # ---------- LOCAL FILE ----------
        if input_type == "Upload Files":
            file_bytes = src.read()
            preview = encode_file(file_bytes, src.type)

            document = {
                "type": "document_url" if "pdf" in src.type else "image_url",
                "document_url" if "pdf" in src.type else "image_url": preview
            }
            name = src.name

        # ---------- URL ----------
        else:
            src = src.strip()
            if not src:
                continue

            document = {
                "type": "document_url" if is_pdf(src) else "image_url",
                "document_url" if is_pdf(src) else "image_url": src
            }
            preview = src
            name = src.split("/")[-1]

        with st.spinner(f"Processing {name}"):
            try:
                text = run_ocr(api_key, document)
                lang = detect_language(text)
            except Exception as e:
                text = f"Error: {e}"
                lang = "unknown"

        st.session_state.results.append({
            "name": name,
            "preview": preview,
            "text": text,
            "language": lang
        })

        progress.progress((i + 1) / len(sources))
        time.sleep(0.5)

# ================= DISPLAY =================
for idx, r in enumerate(st.session_state.results):
    st.divider()
    st.subheader(f"📄 {r['name']} | 🌍 {r['language']}")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Preview", "OCR Text", "Summary", "Ask Question"]
    )

    # ---------- PREVIEW ----------
    with tab1:
        if r["preview"].endswith(".pdf") or "application/pdf" in r["preview"]:
            st.markdown(
                f"<iframe src='{r['preview']}' width='100%' height='600'></iframe>",
                unsafe_allow_html=True
            )
        else:
            st.image(r["preview"])

    # ---------- OCR TEXT ----------
    with tab2:
        search = st.text_input("🔍 Search", key=f"s{idx}")
        text = r["text"]
        if search:
            text = text.replace(search, f"**{search}**")
        st.markdown(text)

        st.markdown(download_link(text, f"{r['name']}.txt", "text/plain"), unsafe_allow_html=True)
        st.markdown(download_link(text, f"{r['name']}.md", "text/markdown"), unsafe_allow_html=True)
        st.markdown(
            download_link(json.dumps(r, indent=2), f"{r['name']}.json", "application/json"),
            unsafe_allow_html=True
        )

    # ---------- SUMMARY ----------
    with tab3:
        if st.button("🧠 Generate Summary", key=f"sum{idx}"):
            st.success(summarize_text(api_key, r["text"]))

    # ---------- Q&A ----------
    with tab4:
        q = st.text_input("❓ Ask a question", key=f"q{idx}")
        if q:
            st.info(qa_text(api_key, r["text"], q))
