import fitz
import pytesseract
from pdf2image import convert_from_bytes
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = ""

    for page_index, page in enumerate(doc):
        page_text = page.get_text().strip()
        if len(page_text) > 50:
            full_text += page_text + "\n\n"
        else:
            images = convert_from_bytes(pdf_bytes, first_page=page_index + 1, last_page=page_index + 1)
            for image in images:
                ocr_text = pytesseract.image_to_string(image, lang="eng+hun")
                full_text += ocr_text + "\n\n"

    doc.close()
    return full_text


def load_and_split_pdf(pdf_bytes: bytes) -> list[str]:
    full_text = extract_text_from_pdf(pdf_bytes)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "],
    )
    return splitter.split_text(full_text)


def build_faiss_index(chunks: list[str]) -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )
    return FAISS.from_texts(chunks, embeddings)