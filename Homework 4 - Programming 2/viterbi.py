import sys

def viterbi(words,tags,W,T,probabilities):
	score = dict()
	backptr = dict()
	probkeys = probabilities.keys()
	for t in xrange(T):
		wordtag = words[0]+' '+tags[t]
		tagbigram = tags[t]+' '+'phi'
		tagword = str(t)+' 0'
		backptr[tagword] = 0
		if wordtag not in probkeys:
			probabilities[wordtag] = '.0001'
			probkeys = probabilities.keys()
		if tagbigram not in probkeys:
			probabilities[tagbigram] = '.0001'
			probkeys = probabilities.keys()
		
		score[tagword] = float(probabilities[wordtag])*float(probabilities[tagbigram])
	
	#print score
	#print backptr
	
	for w in xrange(1,W):
		for t in xrange(T):
			max = -999
			wordtag = words[w]+' '+tags[t]
			tagword = str(t)+' '+str(w)
			for j in xrange(T):
				prevtagword = str(j)+' '+str(w-1)
				tagseq = tags[t]+' '+tags[j]
				if tagseq not in probkeys:
					probabilities[tagseq] = '.0001'
					probkeys = probabilities.keys()
					
				prodval = float(score[prevtagword])*float(probabilities[tagseq])
				#print prodval
				if prodval > max:
					max = prodval
					index = j
			
			if wordtag not in probkeys:
				probabilities[wordtag] = '.0001'
				probkeys = probabilities.keys()
			
			score[tagword] = float(probabilities[wordtag])* float(max)
			backptr[tagword] = index
	
	#print score
	#print backptr
	if W == 1 :
		w = 0
	sequence = dict()
	
	max = -999
	for t in xrange(T):
		tagword = str(t)+' '+str(w)
		if score[tagword] > max:
			max = score[tagword]
			bestseqindex = t
	#print bestseqindex
	sequence[W-1] = bestseqindex
	
	for w in reversed(xrange(W-1)):
		sequence[w] = backptr[str(sequence[w+1]) + ' ' +str(w+1)]
	
	
	return (max, score, sequence, backptr)



def forward(words,tags,W,T,probabilities):
	seqsum = dict()
	probkeys = probabilities.keys()
	for t in xrange(T):
		wordtag = words[0]+' '+tags[t]
		tagbigram = tags[t]+' '+'phi'
		tagword = str(t)+' 0'
		if wordtag not in probkeys:
			probabilities[wordtag] = '.0001'
			probkeys = probabilities.keys()
		if tagbigram not in probkeys:
			probabilities[tagbigram] = '.0001'
			probkeys = probabilities.keys()
		
		seqsum[tagword] = float(probabilities[wordtag])*float(probabilities[tagbigram])
	
	for w in xrange(1,W):
		for t in xrange(T):
			sum = 0
			wordtag = words[w]+' '+tags[t]
			tagword = str(t)+' '+str(w)
			for j in xrange(T):
				prevtagword = str(j)+' '+str(w-1)
				tagseq = tags[t]+' '+tags[j]
				if tagseq not in probkeys:
					probabilities[tagseq] = '.0001'
					probkeys = probabilities.keys()
					
				sum += float(seqsum[prevtagword])*float(probabilities[tagseq])
				
			
			if wordtag not in probkeys:
				probabilities[wordtag] = '.0001'
				probkeys = probabilities.keys()
			
			seqsum[tagword] = float(probabilities[wordtag])* float(sum)
	
	if W == 1:
		w = 0
	seqprob = dict()
	for w in xrange(W):
		for t in xrange(T):
			sum = 0
			wordtag = str(w) +' '+str(t)
			for j in xrange(T):
				tagword = str(j) +' '+str(w)
				sum += float(seqsum[tagword])
			
			tagword = str(t)+' '+str(w)
			seqprob[wordtag] = float(seqsum[tagword])/sum;
	
	return seqprob
	
if __name__ == '__main__':
	
	tags = ['noun','verb','inf','prep']
	#print tags
	file = open(sys.argv[1], 'r')
	probabilities = dict()
	for line in file.readlines():
		line = line.rstrip()
		k = line.rfind(' ')
		probabilities[line[:k]] = line[k+1:]
	file.close()
	
	#print probabilities
	score = dict()
	backptr = dict()
	sequence = dict()
	seqprob = dict()
	
	file = open(sys.argv[2], 'r')
	for line in file.readlines():
		line = line.rstrip()
		words = line.split(' ')
		#print words
		best,score,sequence,backptr = viterbi(words,tags,len(words),len(tags),probabilities)
		seqprob = forward(words,tags,len(words),len(tags),probabilities)
		print 'PROCESSING SENTENCE: '+line,'\n'
		print 'FINAL VITERBI NETWORK'
		for w in xrange(len(words)):
			for t in xrange(len(tags)):
				tagword = str(t)+' '+str(w)
				print 'P('+words[w]+'='+tags[t]+') = '+format(score[tagword],'.10f')
	
		print '\nFINAL BACKPTR NETWORK'
		for w in xrange(1,len(words)):
			for t in xrange(len(tags)):
				tagword = str(t)+' '+str(w)
				print 'Backptr('+words[w]+'='+tags[t]+') = '+tags[backptr[tagword]]	
		
		print '\nBEST TAG SEQUENCE HAS PROBABILITY = '+str(format(best,'.10f'))
		for w in reversed(xrange(len(words))):
			print words[w]+' -> '+tags[sequence[w]]
		
		
		print '\nFORWARD ALGORITHM RESULTS'
		for w in xrange(len(words)):
			for t in xrange(len(tags)):
				wordtag = words[w]+'='+tags[t]
				numwordtag = str(w)+' '+str(t)
				print 'P('+wordtag+') = '+str(format(seqprob[numwordtag],'.10f'))
		print '\n'