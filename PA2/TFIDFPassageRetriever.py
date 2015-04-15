import operator

class TFIDFPassageRetriever():
    
    ''' From the list of top documents figures out the n most relevent passages
    '''
    def GetRelatedPassages(self, question,n):
        topDocuments=question.GetTopDocuments()
        # We gather all the sentences of all the documents and their similarity score
        sentenceRelevance={}
        for document in topDocuments:
            sentenceRelevance.update(document.GetTFIDFSentenceRelevance(question))
	# We sort the sentences by relevance
	sortedSentenceRelevance = sorted(sentenceRelevance.items(), key=operator.itemgetter(1))
	sortedSentenceRelevance.reverse()
	relatedPassages=[]
        for i in range(n):
            relatedPassages.append(sortedSentenceRelevance[i][0])
	return relatedPassages

