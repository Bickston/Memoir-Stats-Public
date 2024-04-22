import re


def get_posts(pdf_text):
    return re.split(r"\b\d{1,2}/\d{1,2}/\d{2} \d{1,2}:\d{2}[AP]M\b", pdf_text)


def clean_text(pdf_text):
    pdf_text = pdf_text.lower()
    characters_to_be_replaced = '''.?!,'’()"“”:$-�%/\\*#=+;[]>{}@~^'''
    for char in characters_to_be_replaced:
        pdf_text = pdf_text.replace(char, "")
    return pdf_text


def track_days(pdf_text, time=False):
    if time:
        return re.findall(r"\b\d{1,2}/\d{1,2}/\d{2} \d{1,2}:\d{2}[AP]M\b", pdf_text)
    return re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', pdf_text)


def get_sentences(pdf_text):
    pdf_text = pdf_text.lower()
    pdf_text = pdf_text.replace("mr.", "mr")
    pdf_text = pdf_text.replace("mrs.", "mrs")
    pdf_text = pdf_text.replace("ms.", "ms")
    pdf_text = pdf_text.replace("vol.", "vol")

    return re.split(r'(?<=\w\.[\s\n])(?=[\w\n])', pdf_text)
