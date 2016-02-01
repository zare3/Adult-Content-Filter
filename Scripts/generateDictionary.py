import os
from json import loads, dumps





keywordsPath = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dictionary/AdultPlusPGKeywords.txt' #path for the bag of words/all.vocabs.txt file
dictionary = set ()
articleDictionary = set ()
normalizedDictionary = set ()


with open(keywordsPath, "r") as word_list:
    dictionary = set(word_list.read().split('\n'))


rootdir = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dataset/website htmls labelled/' # path for /bbc dataset
for subdir, dirs, files in os.walk(rootdir):
	for f in files:
		filePath = os.path.join(subdir, f)
		with open(filePath, "r") as word_list:
			for x in word_list.read().split(' '):
				dictWord = x.split(',', 1)[0]
				dictWord = dictWord.replace('.','')
				dictWord = dictWord.replace('"','')
				dictWord = dictWord.replace('\'','')
				dictWord = dictWord.replace('!','')
				dictWord = dictWord.replace('?','')
				dictWord = dictWord.replace('\n','')
				articleDictionary.add(dictWord)

 

normalizedDictionary = set.intersection(dictionary,articleDictionary)
normalizedDictionary = sorted (normalizedDictionary)

outputPath = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dictionary/htmlsDictionary.txt'
outputPathFileObject = open(outputPath,'w')
for z in dictionary:
	outputPathFileObject.write(str(z))
	outputPathFileObject.write('\n')

outputPathFileObject.close()