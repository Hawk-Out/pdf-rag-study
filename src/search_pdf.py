import chromadb
from sentence_transformers import SentenceTransformer

DATABASE_FOLDER = "chroma_db"
COLLECTION_NAME = "course_notes"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def search_pdf(question: str, result_count: int = 3) -> None:
    """Find the PDF chunks most related to a question."""
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Convert the question into an embedding.
    question_embedding = model.encode(question).tolist()

    # Open the saved vector database.
    client = chromadb.PersistentClient(path=DATABASE_FOLDER)
    collection = client.get_collection(COLLECTION_NAME)

    # Find the most similar stored chunks.
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=result_count,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print(f"\nQuestion: {question}\n")

    for index, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        print(f"--- Result {index} ---")
        print(f"Source: {metadata['source']} | Page: {metadata['page']}")
        print(f"Distance: {distance:.4f}")
        print(f"Text: {document}\n")


if __name__ == "__main__":
    search_pdf("What is a shell script?")

