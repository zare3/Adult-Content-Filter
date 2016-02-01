import sklearn.datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import os


categories = ['adult','non-adult']
container_path = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dataset/website htmls labelled/train/'
trainVector = sklearn.datasets.load_files(container_path, description=None, categories=categories, load_content=True, shuffle=True,  encoding='latin-1', decode_error='strict', random_state=0)
print trainVector.target_names
print len(trainVector.data)
print len(trainVector.filenames)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(trainVector.data)
print X_train_counts.shape
print count_vect.vocabulary_.get(u'algorithm')


tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print X_train_tfidf.shape

clf = MultinomialNB().fit(X_train_tfidf, trainVector.target)



docs_new = [ ]
truth = [ ]
totalNumOfFiles = 0
for address in categories:
	rootdir = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/Dataset/website htmls labelled/test/'+address+'/' # path for /bbc dataset
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			filePath = os.path.join(subdir, file)
			fileObject = open (filePath,'r')
			fileContent = fileObject.read()
			docs_new.append(fileContent)
			truth.append(address)
			totalNumOfFiles += 1
			fileObject.close()


X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)


correct = 0
for idx in range(len(predicted)):
	if trainVector.target_names[predicted[idx]] == truth[idx]:
		correct = correct + 1
print (str(correct) + "/" + str(totalNumOfFiles))
print (100*correct/totalNumOfFiles)


#for doc, category in zip(docs_new, predicted):
#	print('%r => %s' % (doc, trainVector.target_names[category]))
