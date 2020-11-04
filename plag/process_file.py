from docx import Document
from .code.main import process

def process_file(filename):
    if filename.name.endswith('.docx'):
        document = Document(filename)
        fullText = []
        data = ''
        for para in document.paragraphs:
            fullText.append(para.text)
            data = '\n'.join(fullText)
    else:
        data = ''
        for chunk in filename.chunks():
            data += chunk.decode('utf')
    return process(data)
    
     
    
    