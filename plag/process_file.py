from docx import Document
from .code.main import process
from .text_matcher.matcher import Matcher,Text


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
    
     
def compare_two(filename1,filename2):
    if filename1.name.endswith('.docx'):
        document = Document(filename1)
        fullText = []
        data = ''
        for para in document.paragraphs:
            fullText.append(para.text)
            data = '\n'.join(fullText)
    else:
        data = ''
        for chunk in filename1.chunks():
            data += chunk.decode('utf')
    
    if filename2.name.endswith('.docx'):
        document = Document(filename2)
        fullText = []
        data2 = ''
        for para in document.paragraphs:
            fullText.append(para.text)
            data = '\n'.join(fullText)
    else:
        data2 = ''
        for chunk in filename2.chunks():
            data2 += chunk.decode('utf')
    
    ta = Text(data, 'A')
    tb = Text(data2, 'B')

    return Matcher(ta,tb).match()
    
     

    