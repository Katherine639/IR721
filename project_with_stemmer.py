#!/usr/bin/env python3

import os
import math
import time
from nltk.stem import PorterStemmer


def joinSentences(listOfSnetences):
    return ''.join(listOfSnetences)

def readCollection():
    fileToread = "data/ap89_collection"
    file = open(fileToread, "r")

    lines = file.readlines()

    c = True
    i = 0
    docs = {}
    while c:
        if lines[i] == '<DOC>\n':
            i += 1
            if '<DOCNO>' in lines[i]:
                docId = lines[i].split(" ")[1]
                docs[docId] = []
                i +=1
                while lines[i] != '</DOC>\n':
                    while lines[i] != '<TEXT>\n':
                        i +=1
                    i +=1
                    while lines[i] != '</TEXT>\n':
                        line = lines[i].rstrip()
                        docs[docId].append(line)
                        i +=1
                    i +=1
                docs[docId] = joinSentences(docs[docId])
        if i == len(lines)-1:
            c = False
        i +=1
    return docs

a = readCollection()
ndoc = len(a)
nterm = [0 for i in range(ndoc)]

# Stop-words
pstop = "stoplist.txt"
stoplist = []
with open(pstop, 'r') as f:
	for line in f:
		stoplist.append(line.strip())

# Initialize stemmer
stemmer = PorterStemmer()

# Using dictionary to store terms
# Using linked list to store the frequency
dterm = {}

class Node(object):
	def __init__(self):
		self.docID = 0
		self.docFreq = 0
		self.next = None
class List(object):
	def __init__(self):
		self.head = None
		self.length = 0
	# Create a node for a document that has this term
	def append(self, Node):
		if not self.head:
			self.head = Node
		else:
			node = self.head
			while node.next:
				node = node.next
			node.next = Node
		self.length += 1
	# Update the frequency of a term for a specific document
	def update(self, ID):
		node = self.head
		while node is not None:
			if node.docID == ID:
				node.docFreq += 1
				break
			else:
				node = node.next
	# A function that can get the frequency for a term in a specific document
	def getFreq(self, ID):
		node = self.head
		while node is not None:
			if node.docID == ID:
				return node.docFreq
			else:
				node = node.next
		return 0
	# Check if a document has a node for a term
	def hasNode(self, ID):
		node = self.head
		if node is None:
			return False
		while node is not None:
			if node.docID == ID:
				return True
			else:
				node = node.next
		return False
	
	# Print out document number with term frequency
	# I only used it for debugging
	def printout(self):
		node = self.head
		if node is None:
			print("Term does not exist.")
		else:
			while node is not None:
				print("ID:", node.docID, "Posting:", node.docFreq)
				node = node.next
	
    

# Get the document index for a term
def getDocs(term):
	if dterm.__contains__(term):
		return dterm[term].length
	else:
		return 0
# Get term frequency with term and document number
def getPost(term, ID):
	if dterm.__contains__(term):
		return dterm[term].getFreq(ID)
	else:
		return 0
# Compute the TF-IDF
def TFIDF(term):
	global ndoc, nterm
	tf = []
	for i in range(ndoc):
		tf.append(getPost(term, i + 1) / nterm[i])
	if not getDocs(term) == 0:
		idf = math.log(ndoc / getDocs(term))
	else:
		idf = 0
	tfidf = [a * idf for a in tf]
	result = []
	def addzero(a):
		if len(a) == 1:
			return '0' + a
		return a
	for i in range(ndoc):
		result.append([tfidf[i], addzero(str(i + 1)), tf[i], idf])
	result.sort(reverse = True)
	print("--------------------------------------------------------------------")
	print("The result for term \"", end = '')
	print(term, end = '')
	print("\", in the order of TF-IDF:")
	print("  Doc No.       TF       IDF    TF-IDF")
	count = 0
	for info in result:
		print("Document", info[1], end = '')
		print(":", "{:7.4f}".format(info[2]), end = '')
		print(",", "{:7.4f}".format(info[3]), end = '')
		print(",", "{:7.4f}".format(info[0]))
		if not info[0] == 0:
			count += 1
	return count

# Read a document
# Record terms and the number of terms
def readdoc(dno,documents):
    global nterm
    words = documents.split()
    l = len(words)
    for i in range(l):
        words[i] = words[i].lower()
        words[i] = stemmer.stem(words[i])
        if words[i] in stoplist:
            l -= 1
        else:
            if not dterm.__contains__(words[i]):
                dterm[words[i]] = List()
            if not dterm[words[i]].hasNode(dno):
                node = Node()
                node.docID = dno
                dterm[words[i]].append(node)
                dterm[words[i]].update(dno)
    idno = int(dno.split('-')[1])
        
    nterm[idno - 1] = l


def test():
	while 1:
		print("+++ Please input the term you want for query, input \"QUIT\" to exit.")
		print("+++ Inputs except for \"QUIT\" are NOT cASe SEnsItIve,")
		query = input("+++ and will be stemmed with Porter Stemmer from NLTK:\n")
		start_2 = time.time()
		if query == "QUIT":
			break
		else:
			query = query.lower()
			query = stemmer.stem(query)
			count = TFIDF(query)
			global time_1
			end_2 = time.time()
			print(count, "relevant documents were given in", end_2 - start_2 + time_1, "second(s).")
			print("--------------------------------------------------------------------")





            
            
            
#Go through all documents
start_1 = time.time()
for key in a:
    readdoc(key,a[key])      
end_1 = time.time()
time_1 = end_1 - start_1
#test()
