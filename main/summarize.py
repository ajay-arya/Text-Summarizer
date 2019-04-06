import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
 
def read_article(fileName):
    file = open(fileName, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []

    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop() 
    
    return sentences

def sentenceSimilarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    allWords = list(set(sent1 + sent2))
 
    vector1 = [0] * len(allWords)
    vector2 = [0] * len(allWords)
 
    for w in sent1:
        if w in stopwords:
            continue
        vector1[allWords.index(w)] += 1
 
    for w in sent2:
        if w in stopwords:
            continue
        vector2[allWords.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def buildSimilarityMatrix(sentences, stopWords):
    similarityMatrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue 
            similarityMatrix[idx1][idx2] = sentenceSimilarity(sentences[idx1], sentences[idx2], stopWords)

    return similarityMatrix


def generateSummary(fileName, top_n=5):
    stopWords = stopwords.words('english')
    summarizeText = []

    sentences =  read_article(fileName)

    sentenceSimilarityMartix = buildSimilarityMatrix(sentences, stopWords)

    sentenceSimilarityGraph = nx.from_numpy_array(sentenceSimilarityMartix)
    scores = nx.pagerank(sentenceSimilarityGraph)

    rankedSentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    print("Indexes of top rankedSentence order are ", rankedSentence)    

    for i in range(top_n):
      summarizeText.append(" ".join(rankedSentence[i][1]))

    print("Summarize Text: \n", ". ".join(summarizeText))

# generateSummary( "../files/summ.txt", 5)