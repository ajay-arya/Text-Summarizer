import PyPDF2
import re
# from summarize_old import generateSummary
from summarize import generateSummary


def store(text, filePath):
    # print(text)
    summaryFile = open(filePath, 'w')
    summaryFile.write(text)
    summaryFile.close()
    return True

def getSummari(line):
    summary = generateSummary('/./files/summ.txt', line)

def modify(text):
    text = text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
    text = re.sub('[^ .a-zA-Z0-9]', '', text)
    text = re.sub(' +', ' ', text)
    return(store(text, './files/preprosed.txt'))

def convertFile(filename, line):
    object = open(filename, 'rb')
    reader = PyPDF2.PdfFileReader(object)
    totalPages = reader.numPages
    print(totalPages)
    text = ''
    for i in range(totalPages):
        page = reader.getPage(i)
        text += page.extractText()
    # print(text)
    temp = False
    temp = modify(text)
    if(temp):
        print('SENDING INVOKING MODEL')
        summari = getSummari(line)
        final = store(summari, './files/final.txt')
        print()
        print('**********************final**********************')
        print(final)
        print('**********************final**********************')
        return summari
    else:
        return 'error'



# convertFile('./uploadedFiles/Semiar_Synopsis.pdf', 4)