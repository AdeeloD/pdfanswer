import streamlit as st
from dotenv import load_dotenv
from rag import load_and_split_pdf, build_faiss_index, retrieve_top_chunks, generate_answer

load_dotenv()

st.set_page_config(
    page_title="PDFanswer",
    page_icon="🔴",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    header[data-testid="stHeader"] {
    display: none !important;
    }
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        background-color: #ffffff;
        color: #111111;
    }
    .stApp {
        background-color: #ffffff;
    }
    section[data-testid="stSidebar"] {
        background-color: #f7f7f7;
        border-right: 2px solid #cc0000;
    }
    .stChatMessage {
        background-color: #fafafa !important;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 12px;
    }
    .stChatInputContainer, .stChatInput {
        background-color: #ffffff !important;
        border: 2px solid #cc0000 !important;
        border-radius: 8px !important;
        color: #111111 !important;
    }
    .stButton > button {
        background-color: #cc0000;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #ff1a1a;
        color: white;
    }
    .stFileUploader {
        background-color: #fff5f5;
        border: 1px dashed #cc0000;
        border-radius: 8px;
    }
    .stExpander {
        background-color: #fff5f5;
        border: 1px solid #ffcccc;
        border-radius: 8px;
    }
    .stInfo {
        background-color: #fff5f5;
        border-left: 4px solid #cc0000;
        color: #111111;
    }
    .stSuccess {
        background-color: #f0fff4;
        border-left: 4px solid #00cc44;
    }
    .stError {
        background-color: #fff5f5;
        border-left: 4px solid #ff0000;
    }
    h1, h2, h3 {
        color: #cc0000 !important;
    }
    .hero-box {
        background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
        border: 2px solid #cc0000;
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 32px;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #cc0000;
        margin-bottom: 8px;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 16px;
    }
    .badge {
        display: inline-block;
        background-color: #fff0f0;
        border: 1px solid #cc0000;
        color: #cc0000;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

with st.sidebar:
    st.markdown("## 📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file (max. 20MB)",
        type=["pdf"],
        accept_multiple_files=False,
    )

    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > 20:
            st.error(f"File too large ({file_size_mb:.1f} MB). Maximum 20MB allowed.")
        elif uploaded_file.name != st.session_state.pdf_name:
            with st.spinner("⚙️ Processing document..."):
                pdf_bytes = uploaded_file.read()
                chunks = load_and_split_pdf(pdf_bytes)
                vectorstore = build_faiss_index(chunks)
                st.session_state.vectorstore = vectorstore
                st.session_state.pdf_name = uploaded_file.name
                st.session_state.chat_history = []
            st.success(f"✅ Ready! ({len(chunks)} chunks indexed)")

    if st.session_state.pdf_name:
        st.info(f"📄 Active: **{st.session_state.pdf_name}**")

    if st.session_state.chat_history:
        if st.button("🗑️ Clear conversation"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.markdown("<small style='color:#999'>PDFanswer — No registration required. Free to use.</small>", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">🔴 PDFanswer</div>
    <div class="hero-sub">Chat with any PDF instantly — no registration, no limits.</div>
    <span class="badge">📚 Learning support</span>
    <span class="badge">🗂️ Admin & docs</span>
    <span class="badge">⚡ Save time</span>
</div>
""", unsafe_allow_html=True)

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 Source excerpts"):
                for i, source in enumerate(message["sources"]):
                    relevance = max(0, min(100, int((1 - source["score"]) * 100)))
                    st.markdown(f"**Excerpt {i+1}** — relevance: `{relevance}%`")
                    st.text(source["content"])
                    if i < len(message["sources"]) - 1:
                        st.divider()

if st.session_state.vectorstore is None:
    st.markdown("""
    <div style='text-align:center; padding: 60px 0; color: #aaaaaa;'>
        <div style='font-size: 3rem;'>👆</div>
        <div style='font-size: 1.1rem; margin-top: 12px; color: #555;'>Upload a PDF on the left to get started</div>
        <div style='font-size: 0.9rem; margin-top: 8px; color: #999;'>Supports lecture notes, contracts, reports, manuals and more</div>
    </div>
    """, unsafe_allow_html=True)
else:
    user_input = st.chat_input("Ask anything about your document...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                top_chunks = retrieve_top_chunks(st.session_state.vectorstore, user_input, k=3)
                answer = generate_answer(user_input, top_chunks)

            st.markdown(answer)
            with st.expander("📚 Source excerpts"):
                for i, source in enumerate(top_chunks):
                    relevance = max(0, min(100, int((1 - source["score"]) * 100)))
                    st.markdown(f"**Excerpt {i+1}** — relevance: `{relevance}%`")
                    st.text(source["content"])
                    if i < len(top_chunks) - 1:
                        st.divider()

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": top_chunks,
        })