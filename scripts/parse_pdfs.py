import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    pdf_folder = "../data/pdfs"
    output_path = "../data/plan_texts.txt"
    with open(output_path, "w") as out:
        for fname in os.listdir(pdf_folder):
            if fname.endswith(".pdf"):
                path = os.path.join(pdf_folder, fname)
                out.write(f"\n=== {fname} ===\n")
                out.write(extract_text_from_pdf(path))
    print(f"Extracted all PDF texts to {output_path}")

