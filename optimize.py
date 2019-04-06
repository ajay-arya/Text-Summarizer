import PyPDF2
import re
from summarize import generateSummary


def store(text):
    print(text)
    summaryFile = open('./files/summ.txt', 'w')
    summaryFile.write(text)
    summaryFile.close()
    print()
    print()
    return True


def getSummary(line):
    summary = generateSummary('./files/summ.txt', line)
    print(summary)


def modify(text):
    text = text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
    text = re.sub('[^ a-zA-Z0-9.]', '', text)
    text = re.sub(' +', ' ', text)
    return(store(text))


def convertFile(filename, line):
    object = open(filename, 'rb')
    reader = PyPDF2.PdfFileReader(object)
    totalPages = reader.numPages
    print(totalPages)
    text = ''
    for i in range(totalPages):
        page = reader.getPage(i)
        text += page.extractText()
    print(text)
    temp = modify(text)
    if(temp):
        getSummary(line)


convertFile('./uploadedFiles/Semiar_Synopsis.pdf', 4)
