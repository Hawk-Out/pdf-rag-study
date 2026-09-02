from read_pdf import read_pdf_pages
from pathlib import Path

PDF_FOLDER = Path("data")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping character-based chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(pages: list[dict]) -> list[dict]:
    """Create chunks and preserve their source and page metadata."""
    chunks = []

    for page in pages:
        text_chunks = split_text(
            text=page["text"],
            chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP,
        )

        for chunk_number, text in enumerate(text_chunks, start=1):
            chunks.append(
                {
                    "id": f"{page['source']}-page-{page['page']}-chunk-{chunk_number}",
                    "source": page["source"],
                    "page": page["page"],
                    "text": text,
                }
            )

    return chunks


def main() -> None:
    pdf_files = list(PDF_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDF found. Put one PDF inside the data folder.")
        return

    pages = read_pdf_pages(pdf_files[0])
    chunks = create_chunks(pages)

    print(f"Total chunks created: {len(chunks)}")

    for chunk in chunks[:3]:
        print(f"\n--- {chunk['id']} ---")
        print(chunk["text"])


if __name__ == "__main__":
    main()
