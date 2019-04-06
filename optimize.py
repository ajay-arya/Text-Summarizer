import PyPDF2
import re


def store(text):
    print(text)
    summaryFile = open('./files/summ.txt', 'w')
    summaryFile.write(text)
    summaryFile.close()


def modify(text):
    text = text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
    text = re.sub('[^ a-zA-Z0-9.]', '', text)
    store(text)


def convertFile(filename):
    object = open(filename, 'rb')
    reader = PyPDF2.PdfFileReader(object)
    totalPages = reader.numPages
    print(totalPages)
    for i in range(totalPages):
        page = reader.getPage(i)
        text = page.extractText()
        modify(text)


# convertFile('./uploadedFiles/sample1.pdf')
