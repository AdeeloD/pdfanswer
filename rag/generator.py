import os
from groq import Groq


def generate_answer(question: str, context_chunks: list[dict]) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    context_text = "\n\n---\n\n".join(
        [f"[Detail {i+1}]:\n{chunk['content']}" for i, chunk in enumerate(context_chunks)]
    )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer questions using ONLY the provided context. If the answer is not in the context, say 'A dokumentum nem tartalmaz erre vonatkozó információt.' Always answer in the same language as the question."
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {question}"
            }
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    return response.choices[0].message.content
