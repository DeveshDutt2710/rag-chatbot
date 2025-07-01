from docx import Document
import os

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

if __name__ == "__main__":
    docx_path = "../data/America's_Choice_Medical_Questions.docx"
    output_path = "../data/medical_questions.txt"
    text = extract_text_from_docx(docx_path)
    with open(output_path, "w") as f:
        f.write(text)
    print(f"Extracted medical questions to {output_path}")
