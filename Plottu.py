import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

import requests
import pdfplumber
import pandas as pd
import textract

from collections import namedtuple

Inv = namedtuple('a', 'b')


def download_file(url):
    local_filename = url.split('/')[-1]

    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)

    return local_filename


url = "http://www.arbowebforest.com/android/ArboWebForestUserManual.pdf"
web = download_file(url)
with pdfplumber.open(web) as pdf:
    page = pdf.pages[7]
    text = page.extract_text()

# Tokenizing the text 
stopWords = set(stopwords.words("english"))
words = word_tokenize(text)

# Creating a frequency table to keep the  
# score of each word

freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1

# Creating a dictionary to keep the score 
# of each sentence 
sentences = sent_tokenize(text)
sentenceValue = dict()

for sentence in sentences:
    for word, freq in freqTable.items():
        if word in sentence.lower():
            if sentence in sentenceValue:
                sentenceValue[sentence] += freq
            else:
                sentenceValue[sentence] = freq

sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

# Average value of a sentence from the original text 

average = int(sumValues / len(sentenceValue))

# Storing sentences into our summary. 
summary = ""
for sentence in sentences:
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
        summary += " " + sentence
print("SUMMARY:"+"\n \n"+ summary);