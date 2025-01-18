import os
import PyPDF2

def process_pdf(pdf_path):
    text = ""
    try:
       with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
            print(f"Error extracting text from the PDF: {e}")
            return None
    return text

if __name__ == '__main__':
    processed_text = process_pdf("../data/books.pdf")
    if processed_text:
       print("Processed text:\n", processed_text)