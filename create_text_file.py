import fitz


def extract_text_from_pdf(pdf_path, output_txt_path):
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        extracted_text += page.get_text()

    pdf_document.close()

    with open(output_txt_path, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)


def get_extracted_text(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as file:
        return file.read()

