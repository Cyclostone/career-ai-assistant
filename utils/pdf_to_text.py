"""
PDF to Text Converter
Converts all PDF files in data/knowledge/ to .txt files
so they can be deployed to HuggingFace Spaces (which rejects binary files).

Usage: python -m utils.pdf_to_text
"""

from pathlib import Path
from pypdf import PdfReader


KNOWLEDGE_DIR = "data/knowledge"


def convert_pdf_to_text(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(str(pdf_path))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def main():
    knowledge_dir = Path(KNOWLEDGE_DIR)
    if not knowledge_dir.exists():
        print(f"❌ Knowledge directory not found: {knowledge_dir}")
        return

    pdf_files = list(knowledge_dir.glob("*.pdf"))
    if not pdf_files:
        print("⚠️ No PDF files found in knowledge directory")
        return

    print(f"📄 Found {len(pdf_files)} PDF files to convert\n")

    for pdf_path in pdf_files:
        txt_path = pdf_path.with_suffix(".txt")
        print(f"  Converting: {pdf_path.name}")

        try:
            text = convert_pdf_to_text(pdf_path)
            if text:
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"  ✅ Saved: {txt_path.name} ({len(text):,} chars)")
            else:
                print(f"  ⚠️ No text extracted from {pdf_path.name}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n✅ Done! Text files are ready for deployment.")
    print(f"   Next: commit and push, then re-index on HuggingFace.")


if __name__ == "__main__":
    main()
