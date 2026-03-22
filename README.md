# 🔴 PDFanswer

> Chat with any PDF instantly — no registration, no limits.

PDFanswer is an AI-powered document assistant that lets you upload any PDF and ask questions about it in natural language. Built with a full RAG (Retrieval-Augmented Generation) pipeline from scratch.

---

## ✨ Features

- 📄 Upload any PDF up to 20MB
- 🔍 Semantic search using FAISS vector store
- 🤖 Powered by Llama 3.3 70B via Groq API
- 📸 OCR support for scanned/image-based PDFs
- 📚 Source excerpts shown with every answer
- ⚡ No registration, no login, no data stored

---

## 🧠 How It Works
```
PDF Upload → Text Extraction (PyMuPDF + Tesseract OCR)
          → Chunking (RecursiveCharacterTextSplitter)
          → Embedding (all-MiniLM-L6-v2 via sentence-transformers)
          → FAISS Vector Index
          → Semantic Search (top 3 relevant chunks)
          → LLM Answer Generation (Llama 3.3 70B / Groq)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Orchestration | LangChain |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS (in-memory) |
| OCR | Tesseract + pdf2image |
| LLM | Llama 3.3 70B via Groq API |
| Deployment | Docker + AWS EC2 |

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/pdfanswer.git
cd pdfanswer
```

**2. Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
cp .env.example .env
```
Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_key_here
```
Get a free key at: https://console.groq.com

**4. Run**
```bash
streamlit run app.py
```

---

## 🐳 Run with Docker
```bash
docker build -t pdfanswer .
docker run -p 8501:8501 --env-file .env pdfanswer
```

---

## 📁 Project Structure
```
pdfanswer/
├── app.py              ← Streamlit UI
├── rag/
│   ├── ingest.py       ← PDF processing, OCR, embeddings, FAISS index
│   ├── retriever.py    ← Semantic search
│   └── generator.py    ← LLM answer generation
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (free at console.groq.com) |

---

*Built as a portfolio project demonstrating RAG architecture on free infrastructure.*