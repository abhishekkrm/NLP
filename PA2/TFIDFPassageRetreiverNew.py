import operator
from PassageRetriever import IPassageRetriever
from sklearn.feature_extraction.text import TfidfVectorizer

''' Differs from TFIDFPassageRetriever in a way that it uses passages instead of sentences
'''
class TFIDFPassageRetrieverNew(IPassageRetriever):
    
    ''' Returns a dictionary of <Passage> --> <TF-IDF Similarity with the question> for all sentences in document
    '''
    def __GetdocPassageRelevance(self, document, question):
        docPassages = document.GetPassages()
        # Passage list in lowercase  
        docPassages = [passage.lower() for passage in docPassages]
        
        # Get Questionkeywords in lowercase
        questionKeyword = [" ".join(question.GetKeywords()).lower()] 
        
        # Compute the TFIDF similarity between question keywords and Passages
        tfidf = TfidfVectorizer(min_df=1, stop_words='english').fit_transform(questionKeyword+docPassages)
        passageScoreList= (tfidf * tfidf.T).A[0,1:] 
        
        docPassageRelevance={}        
        for i in range(len(docPassages)):
            docPassageRelevance[docPassages[i]] = passageScoreList[i]
            
        return docPassageRelevance
    
    ''' From the list of top documents figures out the n most relevent passages
    '''
    def GetRelatedPassages(self, question, n=10):
        # Gather all the passages of all the documents (top documents for the given question) and their similarity score
        relevantPassages={}

        topDocuments=question.GetTopDocuments()

        for document in topDocuments:
            relevantPassages.update(self.__GetdocPassageRelevance(document, question))
            
        # We sort the sentences by relevance
        sortedRelevantPassage = sorted(relevantPassages.items(), key=operator.itemgetter(1), reverse=True)
        
        relatedPassagesList=[]
        for i in range(n):
            relatedPassagesList.append(sortedRelevantPassage[i][0])
        
        return relatedPassagesList

