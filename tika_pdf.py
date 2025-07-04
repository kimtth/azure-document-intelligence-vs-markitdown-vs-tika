from tika import parser
# https://github.com/chrismattmann/tika-python

def extract_text_from_pdf(pdf_path):
    parsed = parser.from_file(pdf_path)
    return parsed.get("content", "")


if __name__ == "__main__":
    input_file_path = "input/sample.pdf"  # Replace with your PDF file path
    output_text_path = "output/tika_extracted_text.txt"  # Path to save the extracted text
    extracted_text = extract_text_from_pdf(input_file_path)
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
