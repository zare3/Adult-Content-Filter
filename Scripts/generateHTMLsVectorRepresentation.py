import os
from json import loads, dumps





dictPath = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dictionary/wordsMap.txt'
wordsMap = {}
with open(dictPath) as f:
    for line in f:
    	line = line.strip()
    	(key, val) = line.split(' ', 1)
    	wordsMap[val] = int(key)


category  = ['adult', 'non-adult']

listOfVectors = [ ]
maxVecSize = 0

for address in category:
	rootdir = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dataset/website htmls labelled/'+address+'/' # path for /bbc dataset
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			relDir = os.path.relpath(subdir,rootdir)
			relFilePath = os.path.join(relDir, file)
			filePath = os.path.join(subdir, file)
			fileObject = open (filePath,'r')
			fileContent = fileObject.read()
			fileObject.close()

			singleVec = [ ]
			if address == 'adult':
				singleVec.append(0)
			else:
				singleVec.append(1)
			for word in fileContent.split(' '):
				dictWord = word.split(',', 1)[0]
				dictWord = dictWord.replace('.','')
				dictWord = dictWord.replace('"','')
				dictWord = dictWord.replace('\'','')
				dictWord = dictWord.replace('!','')
				dictWord = dictWord.replace('?','')
				dictWord = dictWord.replace('\n','')
				if dictWord in wordsMap:
					singleVec.append(wordsMap[dictWord])
				else:
					singleVec.append(-1)
			if len(singleVec) > 4000:
				continue
			if len(singleVec) > maxVecSize:
				maxVecSize = len(singleVec)
			listOfVectors.append(singleVec)
print maxVecSize
counter = 0
for l in listOfVectors:
	sz = len(l)
	for t in range (0, maxVecSize - sz):
		l.append(0)
	if l[0] == 0:
		outputPath = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dataset/website htmls labelled vector representation/' + 'adult' + '/' + str(counter) + '.txt'
	else:
		outputPath = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dataset/website htmls labelled vector representation/' + 'non-adult' + '/' + str(counter) + '.txt'
	outputPathFileObject = open(outputPath,'w')
	counter = counter + 1
	for idx in range (1,len(l)):
		outputPathFileObject.write(str(l[idx]))
		outputPathFileObject.write('\n')
	outputPathFileObject.close()



