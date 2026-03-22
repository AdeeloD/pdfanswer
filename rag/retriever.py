from langchain_community.vectorstores import FAISS


def retrieve_top_chunks(vectorstore: FAISS, query: str, k: int = 3) -> list[dict]:
    results = vectorstore.similarity_search_with_score(query, k=k)
    return [
        {"content": doc.page_content, "score": float(score)}
        for doc, score in results
    ]
