import os

import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer

DATABASE_FOLDER = "chroma_db"
COLLECTION_NAME = "course_notes"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "openai/gpt-oss-20b"


def retrieve_context(question: str, result_count: int = 3) -> tuple[str, list[dict]]:
    """Retrieve the most relevant PDF chunks and format them as context."""
    model = SentenceTransformer(EMBEDDING_MODEL)
    question_embedding = model.encode(question).tolist()

    client = chromadb.PersistentClient(path=DATABASE_FOLDER)
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=result_count,
        include=["documents", "metadatas"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []
    sources = []

    for document, metadata in zip(documents, metadatas):
        context_parts.append(
            f"Source: {metadata['source']}, Page: {metadata['page']}\n{document}"
        )
        sources.append(metadata)

    return "\n\n---\n\n".join(context_parts), sources


def generate_answer(question: str, context: str) -> str:
    """Ask Groq to answer only from the retrieved PDF context."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY was not found. Set it in the terminal before running."
        )

    client = Groq(api_key=api_key)

    prompt = f"""

You are a helpful university-level teaching assistant.

Answer the user's question using ONLY the information provided in the context.

Write the answer in natural, fluent Banglish
(Bengali written using English/Roman letters).

Do not write Bengali using Bangla script.
Do not produce awkward word-for-word translations from English.
Use simple, conversational Banglish that a Bangladeshi university student
would naturally understand.

Keep technical terms such as Shell, Bash, script, command, interpreter,
Linux, file extension, etc. in English.

Explain technical concepts clearly and simply.

If the answer is not present in the context, say that the information is
not available in the provided PDF.

PDF context:
{context}

User question:
{question}
"""


    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def main() -> None:
    question = input("Ask a question about the PDF: ").strip()

    if not question:
        print("Please enter a question.")
        return

    context, sources = retrieve_context(question)

    print("\nGenerating answer...\n")
    answer = generate_answer(question, context)

    print(answer)


if __name__ == "__main__":
    main()
