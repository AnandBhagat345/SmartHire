import pdfplumber



def extract_text_from_pdf(file : str) -> str:
    text =""
    
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            
            extracted =page.extract_text()
            if extracted is not None:
                text +=extracted + "\n"
    
    return text
    