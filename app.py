from numpy import full
import streamlit as st
import json, time
from ocr_service import run_ocr
from llm_service import summarize_text, qa_text
from utils import LANGUAGE_MAP, encode_file, detect_language, download_link, is_pdf
from config import SUPPORTED_FILES

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Mistral OCR Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 1rem 3rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: white;
    }
    
    /* ================= TAB STYLING ================= */

    /* Tab container */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #000000;
        padding: 8px;
        border-radius: 12px;
    }

    /* Individual tab */
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #1a1a1a;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #333333;
        transition: all 0.25s ease-in-out;
    }

    /* Hover effect */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2b2b2b;
        color: #ffffff;
    }

    /* Selected tab */
    .stTabs [aria-selected="true"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
    }

    /* Remove Streamlit default focus outline */
    .stTabs [data-baseweb="tab"]:focus {
        outline: none;
        box-shadow: none;
    }

    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(102, 126, 234, 0.3);
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #667eea;
        border-radius: 10px;
        color: #333;
        padding: 20px;
        background-color: #f8f9fa;
        margin: 10px 0;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Language badge */
    .language-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 5px 0;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        color: #333;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    
    /* API key input */
    .stTextInput > div > div > input {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.image("ocr.png", width=200)
    st.title("🤖 Mistral OCR Pro")
    st.markdown("---")
    
    st.markdown("### 📋 How to Use")
    with st.expander("Get Started Guide", expanded=True):
        st.markdown("""
        1. **Enter your API Key** in the main panel
        2. **Choose input type** (Upload or URL)
        3. **Upload files** or paste URLs
        4. **Click Run OCR** to extract text
        5. **Explore results** in tabs
        """)
    
    st.markdown("---")
    st.markdown("### 🎯 Features")
    st.markdown("""
    <div class="feature-card">
        📸 Multi-format OCR
        <br><small>PDF, JPG, PNG, TIFF</small>
    </div>
    <div class="feature-card">
        🌍 Auto-language Detection
        <br><small>100+ languages</small>
    </div>
    <div class="feature-card">
        🧠 AI Summarization
        <br><small>Smart text summaries</small>
    </div>
    <div class="feature-card">
        ❓ Interactive Q&A
        <br><small>Ask questions about content</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    if "results" in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Processed Files", len(st.session_state.results))
        with col2:
            st.metric("Supported Formats", len(SUPPORTED_FILES))
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 10px;">
        Academic Group Project 
        <span style="color: #667eea; font-size: 0.9em;">Intelligent Document Processing System</span>
        <br>Version 1.0
    </div>
    """, unsafe_allow_html=True)

# ================= MAIN CONTENT =================
# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div class="header-container">
        <h1 style="color: white; margin: 0;">🤖 Mistral OCR Pro</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem;">
            Advanced OCR with AI-powered text extraction, summarization, and Q&A
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric("Processing Speed", "Fast", "⚡")

# ================= API KEY SECTION =================
st.markdown("### 🔐 Authentication")
with st.container():
    api_key = st.text_input(
        "**Mistral API Key**",
        type="password",
        placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        help="Enter your Mistral AI API key to get started"
    )
    
    if not api_key:
        st.warning("🔒 Please enter your Mistral API Key to proceed")
        with st.expander("ℹ️ How to get your API Key", expanded=True):
            st.markdown("""
            <div style="background: #f8f9fa; color: #333; padding: 15px; border-radius: 10px;">
            1. Sign up at <a href="https://v2.auth.mistral.ai/login" target="_blank">Mistral AI</a><br>
            2. Navigate to API section in account settings<br>
            3. Generate a new API key<br>
            4. Copy & paste it above<br>
            </div>
            """, unsafe_allow_html=True)
        st.stop()

# ================= INPUT SECTION =================
st.markdown("### 📥 Input Source")
input_type = st.radio(
    "Choose input method:",
    ["Upload Files", "URLs"],
    horizontal=True,
    label_visibility="collapsed"
)

uploaded_files = []
urls = []

if input_type == "Upload Files":
    with st.container():
        uploaded_files = st.file_uploader(
            "**Drag and drop or click to upload**",
            type=SUPPORTED_FILES,
            accept_multiple_files=True,
            help=f"Supported formats: {', '.join(SUPPORTED_FILES)}"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) ready for processing")
            for file in uploaded_files:
                st.markdown(f"""
                <div class="uploadedFile">
                    📄 {file.name} <small>({file.size/1024:.1f} KB)</small>
                </div>
                """, unsafe_allow_html=True)

else:
    with st.container():
        urls = st.text_area(
            "**Enter PDF/Image URLs**",
            placeholder="https://example.com/document.pdf\nhttps://example.com/image.png",
            help="Enter one URL per line"
        ).splitlines()
        
        if urls and any(urls):
            valid_urls = [url.strip() for url in urls if url.strip()]
            st.success(f"✅ {len(valid_urls)} URL(s) ready for processing")

# ================= SESSION =================
if "results" not in st.session_state:
    st.session_state.results = []

# ================= RUN OCR BUTTON =================
if st.button("🚀 **Run OCR Processing**", use_container_width=True):
    st.session_state.results.clear()
    sources = uploaded_files if input_type == "Upload Files" else urls

    if not sources or (isinstance(sources, list) and not any(sources)):
        st.warning("⚠️ Please provide at least one file or URL")
        st.stop()

    sources = [s for s in sources if (isinstance(s, str) and s.strip()) or (not isinstance(s, str))]
    
    if not sources:
        st.warning("⚠️ Please provide valid input")
        st.stop()

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.status("📊 **Processing files...**", expanded=True) as status:
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
                status.update(label=f"🔍 Processing: {name}")

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
                status.update(label=f"🌐 Processing: {name}")

            try:
                text = run_ocr(api_key, document)
                lang = detect_language(text)
                status.update(label=f"✅ Completed: {name}")
            except Exception as e:
                text = f"Error: {e}"
                lang = "unknown"
                status.update(label=f"❌ Error: {name}")

            st.session_state.results.append({
                "name": name,
                "preview": preview,
                "text": text,
                "language": lang
            })

            progress_bar.progress((i + 1) / len(sources))
            time.sleep(0.3)

        status.update(label="✅ **Processing complete!**", state="complete")
    
    st.balloons()
    st.success(f"✨ Successfully processed {len(st.session_state.results)} file(s)")

# ================= RESULTS DISPLAY =================
if st.session_state.results:
    st.markdown("### 📊 Processing Results")
    st.markdown(f"**Total files processed:** {len(st.session_state.results)}")
    
    for idx, r in enumerate(st.session_state.results):
        st.markdown("---")
        
        # File header with language badge
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"### 📄 {r['name']}")
        
        with col2:
            language_code = r["language"]
            language_name = LANGUAGE_MAP.get(language_code, "Unknown")
            st.markdown(f'<div class="language-badge">🌍 {language_name}</div>', unsafe_allow_html=True)
        
        with col3:
            with st.popover("📁 Quick Actions"):
                st.download_button(
                    label="📥 Download Text",
                    data=r["text"],
                    file_name=f"{r['name']}.txt",
                    mime="text/plain",
                    key=f"dl_txt_{idx}"
                )
                st.download_button(
                    label="📥 Download JSON",
                    data=json.dumps(r, indent=2),
                    file_name=f"{r['name']}.json",
                    mime="application/json",
                    key=f"dl_json_{idx}"
                )
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(
            ["👁️ Preview", "📝 Extracted Text", "🧠 AI Summary", "❓ Q&A"]
        )
        
        # ---------- PREVIEW ----------
        with tab1:
            if r["preview"].endswith(".pdf") or "application/pdf" in r["preview"]:
                st.markdown(
                    f"<iframe src='{r['preview']}' width='100%' height='700' style='border-radius: 10px;'></iframe>",
                    unsafe_allow_html=True
                )
            else:
                st.image(r["preview"])
        
        # ---------- EXTRACTED TEXT ----------
        with tab2:
            search_col, export_col = st.columns([3, 1])
            with search_col:
                search = st.text_input(
                    "🔍 Search in text",
                    placeholder="Type to search...",
                    key=f"search_{idx}"
                )
            
            with export_col:
                st.download_button(
                    "📥 Export as Markdown",
                    data=r["text"],
                    file_name=f"{r['name']}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            # Display text with highlighting
            text_display = r["text"]
            if search:
                text_display = text_display.replace(
                    search, 
                    f"<mark style='background-color: #ffeb3b;'>{search}</mark>"
                )
            
            st.markdown(
                f"""
                <div style='
                    background: #f8f9fa;
                    color: #333;
                    padding: 20px;
                    border-radius: 10px;
                    max-height: 500px;
                    overflow-y: auto;
                    font-family: monospace;
                    font-size: 14px;
                    line-height: 1.6;
                    white-space: pre-wrap;
                '>
                    {text_display}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.caption(f"📏 Character count: {len(r['text']):,}")
        
        # ---------- SUMMARY ----------
        with tab3:
            if st.button("✨ Generate Summary", key=f"sum_{idx}", use_container_width=True):
                with st.spinner("🤖 Generating summary..."):
                    summary = summarize_text(api_key, r["text"])
                    st.markdown(
                        f"""
                        <div style='
                            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                            color: #333;
                            padding: 25px;
                            border-radius: 10px;
                            border-left: 5px solid #667eea;
                        '>
                            <h4 style='margin-top: 0;'>📋 AI Summary</h4>
                            {summary}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.download_button(
                        "📥 Download Summary",
                        data=summary,
                        file_name=f"{r['name']}_summary.txt",
                        mime="text/plain",
                        key=f"dl_sum_{idx}"
                    )
            else:
                st.info("Click the button above to generate an AI summary of the extracted text")
        
        # ---------- Q&A ----------
        with tab4:
            question = st.text_input(
                "💭 Ask a question about the document:",
                placeholder="What is the main topic of this document?",
                key=f"q_{idx}"
            )
            
            if question:
                with st.spinner("🤖 Thinking..."):
                    answer = qa_text(api_key, r["text"], question)
                    st.markdown(
                        f"""
                        <div style='
                            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                            color: #333;
                            padding: 25px;
                            border-radius: 10px;
                            margin-top: 20px;
                        '>
                            <h4 style='margin-top: 0; color: #003366'>❓ Your Question</h4>
                            <p style='background: white; padding: 10px; border-radius: 5px;'>{question}</p>
                            <h4 style='margin-top: 20px; color: #003366'>🤖 Answer</h4>
                            <p style='background: white; color: #006699; padding: 15px; border-radius: 5px; font-size: 16px;'>{answer}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# Empty state when no results
elif api_key:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h3 style="color: #666;">📁 No files processed yet</h3>
            <p style="color: #888;">
                Upload files or enter URLs above and click 
                <span style="color: #667eea; font-weight: bold;">"Run OCR Processing"</span>
                <br>to extract text and unlock AI features
            </p>
            <div style="font-size: 100px;">📄➡️🤖</div>
        </div>
        """, unsafe_allow_html=True)