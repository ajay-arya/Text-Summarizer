import PyPDF2
import re
# from summarize_old import generateSummary
from summarize import generateSummary

data = []
data.append('') # Data with preprocessed text
data.append('') # Data with summarized text

def store(text, filePath):
    # print(text)
    summaryFile = open(filePath, 'w')
    summaryFile.write(text)
    summaryFile.close()
    return True

def getSummari(line):
    summary = generateSummary('./files/preprosed.txt', line)
    return summary

def modify(text):
    global data
    text = text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
    text = re.sub('[^ .a-zA-Z0-9]', '', text)
    text = re.sub(' +', ' ', text) 
    data[0] = text
    return(store(text, './files/preprosed.txt'))

def convertFile(filename, line):
    global data
    objects = open(filename, 'rb')
    reader = PyPDF2.PdfFileReader(objects)
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
        summary = getSummari(line)
        final = store(summary, './files/final.txt')
        data[1] = summary
        return data
    else:
        return 'error'

def optimizeWiki(text, line):
    temp = False
    temp = store(text, './files/wiki.txt')
    if temp:
        modifyer = False
        modifyer = modify(text)
        if modifyer:
            summary = getSummari(line)
            final = store(summary, './files/final.txt')
            data[1] = summary
            return data
        else:
            return 'error'
