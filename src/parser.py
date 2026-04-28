import io
import fitz  # PyMuPDF
import docx

def parse_pdf(file_obj) -> str:
    """
    Parses a PDF file object and returns the extracted text.
    """
    text = ""
    try:
        # Streamlit's uploaded file can be read as bytes
        file_bytes = file_obj.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text

def parse_docx(file_obj) -> str:
    """
    Parses a DOCX file object and returns the extracted text.
    """
    text = ""
    try:
        doc = docx.Document(file_obj)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
    return text

def extract_text_from_file(file_obj, filename: str) -> str:
    """
    Determines file type from filename and extracts text.
    """
    file_extension = filename.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return parse_pdf(file_obj)
    elif file_extension in ['doc', 'docx']:
        return parse_docx(file_obj)
    else:
        # Fallback or unsupported
        try:
            return file_obj.read().decode('utf-8')
        except:
            return ""
