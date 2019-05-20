# Importing packages
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk


# Declaring Porter Stemmer
from nltk.stem import PorterStemmer
ps = PorterStemmer()

# Reading the file
def genatateSummary(fileName):
    file = open('./files/summ.txt', 'r') 
    text = file.read()

# Defining Stopwords
stopWords = set(stopwords.words("english"))


# Tokenizing text to word and using Porter Stemmer to stem to root word
words = word_tokenize(text)
for word in words:
    ps.stem(word)

import re as re
# Creating frequency table of words
freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1


        
#***************************
# To find weighted frequency      
max_freq = max(freqTable.values())

for word in freqTable.keys():  
    freqTable[word] = (freqTable[word]/max_freq)        
#***************************        
        
# Tokenizing The text to sentences    
sentences = sent_tokenize(text)
sentenceRank = dict()


# Ranking the sentences
word_count = 0
for sentence in sentences:
    for word, freq in freqTable.items():
        if word in sentence.lower():
            word_count = word_count + 1
            if sentence in sentenceRank:
                sentenceRank[sentence] += freq
            else:
                sentenceRank[sentence] = freq
    sentenceRank[sentence] = sentenceRank[sentence]
    word_count = 0


# Sorting sentence and rank dictionary 
import operator
sentenceRank_list = sorted(sentenceRank.items(), key=operator.itemgetter(1))
sentenceRank_list = sentenceRank_list[::-1]


# Generating and printing the Summary
summary = ''
num_of_sentences = 5
for q in range(num_of_sentences):
    summary += " " + sentenceRank_list[q][0]
print(summary)


# Threshold_based = False
# if(Threshold_based):
# sumValues = 0
#     for sentence in sentenceRank:
#         sumValues += sentenceRank[sentence]
#         print(sentenceRank[sentence])

#     # Average value of a sentence from original text
#     average = int(sumValues / len(sentenceRank))
#     print(average)

#     summary = ''
#     for sentence in sentences:
#         if (sentence in sentenceRank) and (sentenceRank[sentence] > 1.5*average):
#             summary += " " + sentence
#     print(summary)