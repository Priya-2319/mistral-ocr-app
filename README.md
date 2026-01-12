# 🤖 Mistral OCR – Intelligent Document Processing System

An AI-powered Optical Character Recognition (OCR) web application built using **Mistral OCR**, **Streamlit**, and **Natural Language Processing (NLP)**.  
This system extracts text from **PDFs and images** (via upload or URL) and provides advanced features such as **summarization, question answering, search, and multi-format export**.

---

## 📌 Project Overview

Manual data extraction from documents is time-consuming and error-prone.  
This project solves that problem by providing an **intelligent OCR platform** that converts unstructured documents into meaningful, searchable, and analyzable text using modern AI models.

The application is designed as a **college-level project** with clean architecture, scalability, and real-world relevance.

---

## ✨ Key Features

- 📄 OCR for **PDFs and Images**
- 🌐 Supports **Local Uploads & URLs**
- 🔍 Search within extracted text
- 🧠 AI-powered **Text Summarization**
- ❓ Ask Questions on OCR Text (Q&A)
- 🌍 Automatic **Language Detection**
- ⬇️ Export results as **TXT, Markdown, JSON**
- 👁️ Document Preview (PDF/Image)
- ⚡ Batch processing with progress tracking
- 🧩 Modular & clean code structure

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI Models:** Mistral OCR, Mistral LLM  
- **Libraries:**  
  - `mistralai`
  - `langdetect`
  - `python-docx`
  - `streamlit`

---

## 📁 Project Structure

```
mistral_ocr_app/
├── app.py              # Main Streamlit application
├── ocr_service.py      # OCR logic using Mistral
├── llm_service.py      # Summarization & Q&A
├── utils.py            # Helper utilities
├── config.py           # Configuration & constants
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com//mistral-ocr-app.git
cd mistral-ocr-app
```

### 2️⃣ Create Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Setup

You need a **Mistral API Key**.

1. Get your API key from: [https://mistral.ai](https://mistral.ai)
2. Enter the API key in the app UI when prompted

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at:
```
http://localhost:8501
```

---

## 📄 How to Use

1. **Enter your Mistral API Key**
2. **Choose input type:**
   - Upload Files (PDF/Image)
   - Enter Document URLs
3. **Click Run OCR**
4. **Preview document and extracted text**
5. **Use advanced features:**
   - Search text
   - Generate summary
   - Ask questions
   - Download results in preferred format

---

## 📜 License

MIT License