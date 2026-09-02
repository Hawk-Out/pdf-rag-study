from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from chunk_pdf import create_chunks
from read_pdf import read_pdf_pages

PDF_FOLDER = Path("data")
DATABASE_FOLDER = Path("chroma_db")
COLLECTION_NAME = "course_notes"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def main() -> None:
    pdf_files = list(PDF_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDF found. Put one PDF inside the data folder.")
        return

    # 1. Read the PDF and split it into chunks
    pages = read_pdf_pages(pdf_files[0])
    chunks = create_chunks(pages)

    # 2. Load the embedding model
    print("Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # 3. Convert chunk text into embeddings
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts).tolist()

    # 4. Create/open a local ChromaDB database
    client = chromadb.PersistentClient(path=str(DATABASE_FOLDER))

    # Remove the old collection so rerunning does not create duplicate chunks
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    # 5. Store embeddings, text, and source metadata
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {
                "source": chunk["source"],
                "page": chunk["page"],
            }
            for chunk in chunks
        ],
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")
    print(f"Database folder created: {DATABASE_FOLDER}")


if __name__ == "__main__":
    main()
	
