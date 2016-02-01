import os
from json import loads, dumps





keywordsPath = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dictionary/htmlsDictionary.txt' #path for the bag of words/all.vocabs.txt file
dictionary = set ()

wordMap = {}


with open(keywordsPath, "r") as word_list:
    dictionary = set(word_list.read().split('\n'))

counter = 1
for word in dictionary:
	wordMap[counter] = word
	counter += 1
	

outputPath = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dictionary/wordsMap.txt'
outputPathFileObject = open(outputPath,'w')
for key, value in wordMap.iteritems():
	outputPathFileObject.write(str(key))
	outputPathFileObject.write(' ')
	outputPathFileObject.write(value)
	outputPathFileObject.write('\n')

outputPathFileObject.close()