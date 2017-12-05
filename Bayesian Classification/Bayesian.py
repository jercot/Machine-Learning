# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 22:18:49 2017

@author: Jeremiah
"""
import math
import os
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import ngrams

number = 0
posWords, negWords = ([] for i in range(2))
posDict, negDict, posFreq, negFreq = ({},)*4
paths = ['LargeIMDB\\', 'SmallIMDB\\']
words = set()
stopwords = ["br", "i", "s", "t", "ve", "ll", "re", "ve", "d", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
tokExp = '\w+'

def readFile(path):
    file = open(path, "r", encoding = "utf8")
    fileContent = file.read()
    fileContent = fileContent.lower()
    tkn = RegexpTokenizer(tokExp)
    fileContent = tkn.tokenize(fileContent)
    fc2 = ngrams(fileContent, 3)
    fc2 = [ ' '.join(grams) for grams in fc2]
    fileContent.extend(fc2)
    return fileContent

def readDir(path, array):
    for file in os.listdir(path):
        array.extend(readFile(path + file))
    array = [WordNetLemmatizer().lemmatize(word) for word in array]

def countWords(array, dic):
    for word in array:
        if word in words:
            dic[word] += 1

def calcFreq(dicCount, dicFreq):
    total = sum(dicCount.values())
    for word in words:
        dicFreq[word] = math.log((dicCount[word]+1)/(total+len(words)))
        
def readUnknown(path):
    total, pos, neg = (0,)*3
    for file in os.listdir(path):
        negScore,posScore = (0,)*2
        fileContent = readFile(path + file)
        fileContent = [WordNetLemmatizer().lemmatize(word) for word in fileContent]
        for word in fileContent:
            if word in words:
                posScore += posFreq[word]
                negScore += negFreq[word]
        if(negScore < posScore):
            pos += 1
        else:
            neg += 1
        total += 1
    print("Pos - ", (pos/total)*100, " Neg - ", (neg/total)*100)
    
while number<1 or number>2:
    nb = input('Which data set do you want to use?\n1: Large Set\n2: Small Set\n')
    try:
        number = int(nb)
        if number<1 or number>2:
            print("Outside Range")
    except ValueError:
        print("Invalid number")
        
readDir(paths[number-1] + "pos\\", posWords)
readDir(paths[number-1] + "neg\\", negWords)

words = set(posWords + negWords).difference(stopwords)

posDict, negDict = (dict.fromkeys(words, 0) for i in range(2))

countWords(posWords, posDict)
countWords(negWords, negDict)
    
posFreq = dict(posDict)
negFreq = dict(negDict)

calcFreq(posDict, posFreq)
calcFreq(negDict, negFreq)

readUnknown("smallTest\\pos\\")
readUnknown("smallTest\\neg\\")