import operator
import Utils
from PassageRetriever import IPassageRetriever
from sklearn.feature_extraction.text import TfidfVectorizer

class PassageRetrieverImpl2(IPassageRetriever):

    def __GetKeyWordsList(self, text, listtag={'NN','NNP','NNS','PRP','VBP','VBN','VBG','JJR','JJ','RB','FW'}):
        pos_tags = Utils.POSTag(text)
        result_keywords = [word_tag[0] for word_tag in pos_tags if word_tag[1] in listtag]
        if len(result_keywords) == 0:
            result_keywords = Utils.RemoveStopwords(text).split()
        return result_keywords
   
    ''' Returns a dictionary of <Sentence> --> <TF-IDF Similarity with the question> for all sentences in document
    '''
    def __GetdocSentenceRelevance(self, document, question_keywords):
        docSentences = document.GetSentences()
        # Passage list in lowercase  
        docSentences = [passage.lower() for passage in docSentences]
        
        # Compute the TFIDF similarity between question keywords and Passages
        tfidf = TfidfVectorizer(min_df=1, stop_words='english', ngram_range=(2,3)).fit_transform(question_keywords + docSentences)
        scoreList= (tfidf * tfidf.T).A[0,1:] 
        
        docSentenceRelevance={}        
        for i in range(len(docSentences)):
            docSentenceRelevance[docSentences[i]] = scoreList[i]
            
        return docSentenceRelevance
    
    ''' From the list of top documents figures out the n most relevent passages
    '''
    def GetRelatedPassages(self, question, n=10):
        # Gather all the passages of all the documents (top documents for the given question) and their similarity score
        relevantPassages={}
        
        # Get Questionkeywords in lowercase
        question_keywords = [" ".join(self.__GetKeyWordsList(question.GetRawQuestion())).lower()] 
        
        topDocuments=question.GetTopDocuments()

        for document in topDocuments:
            relevantPassages.update(self.__GetdocSentenceRelevance(document, question_keywords))
            
        # We sort the sentences by relevance
        sortedRelevantPassage = sorted(relevantPassages.items(), key=operator.itemgetter(1), reverse=True)
        
        relatedPassagesList=[]
        for i in range(n):
            relatedPassagesList.append(sortedRelevantPassage[i][0])
        
        return relatedPassagesList

