from pathlib import Path
from pypdf import PdfReader

PDF_FOLDER = Path("data")


def read_pdf_pages(pdf_path: Path) -> list[dict]:
    """Extract text and page numbers from one PDF."""
    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                {
                    "source": pdf_path.name,
                    "page": page_number,
                    "text": text.strip(),
                }
            )

    return pages


def main() -> None:
    pdf_files = list(PDF_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDF found. Put one PDF inside the data folder.")
        return

    pdf_path = pdf_files[0]
    pages = read_pdf_pages(pdf_path)

    print(f"PDF: {pdf_path.name}")
    print(f"Pages with text: {len(pages)}")

    for page in pages[:2]:
        preview = page["text"][:300].replace("\n", " ")
        print(f"\n--- Page {page['page']} ---")
        print(preview)


if __name__ == "__main__":
    main()
