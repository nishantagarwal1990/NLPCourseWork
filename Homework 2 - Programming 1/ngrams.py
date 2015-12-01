#!/usr/bin/python

import sys
from math import log
import random
from collections import OrderedDict

def createunigramfrequencytable(filename,unigramtable) :
	try:
		file = open(filename, 'r')
	except:
		print "Could not open file\n"
	
	start = "START"
	unigramtable[start] = 0
	for line in file.readlines():
		unigramtable[start] += 1
		words = line.lower().split()
		for word in words:
			if word not in unigramtable:
				unigramtable[word] = 1
			else:
				unigramtable[word] += 1
				

def createbigramfrequencytable(filename,bigramtable) :
	try:
		file = open(filename, 'r')
	except:
		print "Could not open file\n"
	
	for line in file.readlines():
		words = line.lower().split()
		prev_word = "START"
		for word in words:
			bigram = prev_word + ' ' + word
			if bigram not in bigramtable:
				bigramtable[bigram] = 1
			else:
				bigramtable[bigram] += 1
			prev_word = word


def sumoffrequencies(unigramtable) :
	totuni = 0
	totbi = 0
	start = "START"
	for key in unigramtable:
		if key != start:
			totuni += unigramtable[key]
	return totuni

def probabilityofunigram(line, unigramtable, totalunigramfreqcount) :
	logprob = 0.0
	words = line.lower().split()
	for word in words:
		logprob += log((float(unigramtable[word])/totalunigramfreqcount), 2)
	
	print "Unigrams : logprob(S) = ",round(logprob,4)
	
def probabilityofbigram(line,bigramtable, unigramtable, totalunigramfreqcount) :
	logprob = 0.0
	undefined = 0
	prev_word = "START"
	words = line.lower().split()
	for word in words:
		bigram = prev_word + ' ' + word
		if (bigram not in bigramtable):
			undefined = 1
			break
		else:
			logprob += log((float(bigramtable[bigram])/unigramtable[prev_word]), 2)
		prev_word = word
	
	if undefined == 1:
		print "Bigrams : logprob(S) = undefined"
	else:
		print "Bigrams : logprob(S) = ",round(logprob,4)

def probabilityofbigramwithsmoothing(line, bigramtable,unigramtable, \
	totalunigramfreqcount) :
	logprob = 0.0
	prev_word = "START"
	words = line.lower().split()
	for word in words:
		bigram = prev_word + ' ' + word
		if (bigram not in bigramtable):
			logprob += log(float(1)/(unigramtable[prev_word] + len(unigramtable) - 1),2)
		else:
			logprob += log((float(bigramtable[bigram] + 1)/(unigramtable[prev_word] + \
						len(unigramtable) - 1)),2)
		prev_word = word
	
	print "Smoothed Bigrams : logprob(S) = ",round(logprob,4)
	
def ngramlanguagegenerator(seed,bigramtable,sentence,count) :
	seed = seed.rstrip().lower()
	#print seed
	totfreq = 0
	seeddict = dict()
	sortedseeddict = dict()
	
	for key in bigramtable:
		word = key.split()
		#print word[0]
		if word[0] == seed:
			seeddict[key] = bigramtable[key]
			totfreq += bigramtable[key]
	
	if len(seeddict) == 0:
		return sentence
	
	for key in seeddict:
		seeddict[key] = float(seeddict[key])/totfreq
		
	sortedseeddict = OrderedDict(sorted(seeddict.items(), key=lambda x: x[1]))
	
	num = random.random()
	#print num
	prev_val = 0.0
	for key,value in sortedseeddict.items():
		#print key,value
		if (num > prev_val and num <= value) or (key == sortedseeddict.keys()[-1]):
			sentence += seed + ' '
			#print sentence
			count += 1
			word = key.split()
			if count != 41:
				if word[0] in ['.','?','!']:
					sentence +=  word[0]
					return sentence
				else:
					sentence =  ngramlanguagegenerator(word[1], bigramtable, sentence, count)
					return sentence
			else:
				#print "Exited because of ",count
				return sentence
		prev_val = value
		
	return sentence
			
	

if __name__ == '__main__':
	unigramtable = dict()
	
	bigramtable = dict()
	
	createunigramfrequencytable(sys.argv[1],unigramtable)
	createbigramfrequencytable(sys.argv[1],bigramtable)
	totalunigramfreqcount = sumoffrequencies(unigramtable)
	
	#file = open(sys.argv[2], 'r')
	
	#for line in file.readlines():
		#print "\nS = ",line
		#probabilityofunigram(line, unigramtable, totalunigramfreqcount)
		#probabilityofbigram(line, bigramtable, unigramtable, totalunigramfreqcount)
		#probabilityofbigramwithsmoothing(line, bigramtable,unigramtable, \
		#totalunigramfreqcount)
		
	#file.close()
	
	file = open(sys.argv[3], 'r')
	
	for line in file.readlines():
		print "\nSeed = ",line,"\n"
		for i in xrange(1,11):
			count = 0
			sentence = ""
			sentence = ngramlanguagegenerator(line,bigramtable,sentence,count)
			print "Sentence ",i," : ",sentence
			
	file.close()