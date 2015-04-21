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
    
    
    ''' From the list of top documents figures out the n most relevent passages and their similarity scores
    '''
    def GetRelatedPassages(self, question, n = 10):
        # Gather all the passages of all the documents (top documents for the given question) and their similarity score
        docSentences = []
        docSentencesOrg = []
        docSentenceRelevance = {}
        
        # Get Questionkeywords in lowercase
        question_keywords = [" ".join(self.__GetKeyWordsList(question.GetRawQuestion())).lower()]
        
        topDocuments=question.GetTopDocuments()
        
        for document in topDocuments:
            for sentence in document.GetSentences():
                docSentences.append(sentence.lower())
                docSentencesOrg.append(sentence)
                
        #calculate TFIDF similarity
        tfidf = TfidfVectorizer(min_df=1, stop_words='english', ngram_range=(2,3)).fit_transform(question_keywords + docSentences)
        scoreList= (tfidf * tfidf.T).A[0,1:]
        
        for i in range(len(docSentences)):
            docSentenceRelevance[docSentencesOrg[i]] = scoreList[i]
            
        sortedSentenceRelevance = sorted(docSentenceRelevance.items(), key=operator.itemgetter(1), reverse=True)
        relatedPassagesList = [(sentence_score[0], sentence_score[1]) for sentence_score in sortedSentenceRelevance]

        return relatedPassagesList[:n]