import Utils
import operator
from PassageRetriever import IPassageRetriever
from sklearn.feature_extraction.text import TfidfVectorizer

class PassageRetrieverImpl3(IPassageRetriever):
    ''' Returns a dictionary of <Sentence> --> <TF-IDF Similarity with the question> for all sentences in document
    '''
    def __GetTFIDFSentenceRelevance(self, document, question):
        documentSentences = document.GetSentences()
        
        # Remove stop words from question and set to lowercase
        questionCleared = Utils.RemoveStopwords(question.GetRawQuestion().lower())
        
        # Remove stop words from document sentences and set to lowercase
        sentencesCleared=[]
        for sentence in documentSentences:
            sentencesCleared.append(Utils.RemoveStopwords(sentence.lower()))
        
        # Compute the TFIDF similarity between the question and the sentences
        vectorizer = TfidfVectorizer(min_df=1)
        tfidf = vectorizer.fit_transform([questionCleared]+sentencesCleared)
        score= (tfidf * tfidf.T).A[0,1:]
        
        sentenceRelevance={}        
        for i in range(len(sentencesCleared)):
            sentenceRelevance[documentSentences[i]] = score[i]
            
        return sentenceRelevance
    
    ''' From the list of top documents figures out the n most relevent passages
    '''
    def GetRelatedPassages(self, question, n = 10):
        # Gather all the sentences of all the documents (top documents for the given question) and their similarity score
        sentenceRelevance={}
        
        topDocuments=question.GetTopDocuments()
        for document in topDocuments:
            sentenceRelevance.update(self.__GetTFIDFSentenceRelevance(document, question))
            
        # We sort the sentences by relevance
        sortedSentenceRelevance = sorted(sentenceRelevance.items(), key=operator.itemgetter(1), reverse=True)
        relatedPassagesList = [(sentence_score[0], sentence_score[1]) for sentence_score in sortedSentenceRelevance]

        return relatedPassagesList[:n]