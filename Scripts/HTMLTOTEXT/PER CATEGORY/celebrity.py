from __future__ import with_statement # Required in 2.5
from bs4 import BeautifulSoup
import urllib2
import signal
from contextlib import contextmanager
import os
import sys
import re

try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
except ImportError:
    print '[!] You need to install nltk (http://nltk.org/index.html)'


relativePath = '/Users/Home/AUC/Fall 15/Independent Study/Site Labeler/'


#----------------------------------------------------------------------
def _calculate_languages_ratios(text):
  
    languages_ratios = {}

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    #  Compute  per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios


#----------------------------------------------------------------------
def detect_language(text):
 
    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language

#----------------------------------------------------------------------
class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

#----------------------------------------------------------------------

currFileName = os.path.basename(__file__).rpartition('.')[0]
root = relativePath + 'Dataset/website list labelled/'
scriptDumpPath = relativePath + 'Scripts/HTMLTOTEXT/dump.txt'
scriptDump = open (scriptDumpPath,'w')
dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
counter = 0
processed = 0
start = 0
for folder in dirlist:
	filePath = root + folder + '/domains'
	fileObject = open (filePath,'r')
	fileContent = fileObject.read()
	fileObject.close()
	ans = fileContent.split('\n')
	for el in ans:
		if processed % 100 == 0:
			print (str(processed) + " " + el)
		processed = processed + 1
		#99400 accessoires-erotiques.fr
		try: 
			directory = relativePath +'Dataset/website htmls labelled/' + folder
			if not os.path.exists(directory):
				os.makedirs(directory)
			outPath = relativePath + 'Dataset/website htmls labelled/' + folder + '/' + el +'.txt'
			if el == "fotosdasfamosas.com":
				start = 1
			if os.path.exists(outPath) or not folder == currFileName or start == 0:
				continue
			url = 'https://www.' + el
			try:
				with time_limit(10):
					soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
					for script in soup(["script", "style"]):
						script.extract()
					text = soup.get_text()
					lines = (line.strip() for line in text.splitlines())
					chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
					text = '\n'.join(chunk for chunk in chunks if chunk)
					text = text.encode('utf-8')
			except TimeoutException, msg:
				#print str(processed) + "Timed out!"
				pass
			lang = detect_language(text)	
			if lang == "english" and len(text) > 1000 and "Parallels Plesk" not in text and "Apache" not in text and "404" not in text and "Hosting" not in text and "hosting" not in text:
				outputPathFileObject = open (outPath,'w')
				outputPathFileObject.write(url)
				outputPathFileObject.write('\n')
				outputPathFileObject.write(text)
				counter = counter + 1
				outputPathFileObject.close()
		except:
			pass
scriptDump.close()
