import os
import sys
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def save_text_to_file(file_path, text):
    text_file = open(file_path, 'w')
    text_file.write(text)
    text_file.close()

def process_pdf_files_in_dir(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            print(f"Processing file: {filename}...")
            pdf_path = os.path.join(directory, filename)
            text = extract_text_from_pdf(pdf_path)
            txt_filename = f"{os.path.splitext(filename)[0]}.txt"
            txt_path = os.path.join(directory, txt_filename)
            save_text_to_file(txt_path, text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_to_txt_argv.py <directory>")
        sys.exit(1)
    directory = sys.argv[1]
    process_pdf_files_in_dir(directory)
