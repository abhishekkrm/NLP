from abc import ABCMeta

class IPassageRetriever(metaclass=ABCMeta):
    
    ''' From the list of top documents figures out the relevent passages
    '''
    def GetRelatedPassages(self, question):
        firstDoc=question.GetTopDocuments()[0]
	sentenceRelevance=firstDoc.GetSentenceRelevance(question)
	for sentence in sentenceRelevance:
            print str(sentenceRelevance[sentence])+" "+sentence
