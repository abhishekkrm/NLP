import Utils
import operator
from PassageRetriever import IPassageRetriever
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import wordnet as wn

class TFIDFPassageRetriever(IPassageRetriever):
    
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
    def GetRelatedPassages(self, question, n=10):
        # Gather all the sentences of all the documents (top documents for the given question) and their similarity score
        
        question_text = self.GetExpandedQuestion(question)
        print("Expanded question : "+question_text)
        sentenceRelevance={}
        corpus = []
        corpus.append(question_text)
        topDocuments=question.GetTopDocuments()
        for document in topDocuments:
            #sentenceRelevance.update(self.__GetTFIDFSentenceRelevance(document, question))
            for sentence in document.GetPassages():
                corpus.append(sentence)
            #corpus.append(document.GetText())
        print("Number of sentences in corpus : "+str(len(corpus)))
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(corpus)
        #print(tfidf_matrix_train)
        
        similarity_scores = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)
        #print ("cosine scores ==> "+str(similarity_scores))
        i =0; 
        print("score length : "+str(len(similarity_scores[0])))
        for score in similarity_scores[0]:
            sentenceRelevance[corpus[i]] = score
            i=i+1
            
        # We sort the sentences by relevance
        sortedSentenceRelevance = sorted(sentenceRelevance.items(), key=operator.itemgetter(1), reverse=True)
        
        relatedPassages=[]
        for i in range(n):
            relatedPassages.append(sortedSentenceRelevance[i+1][0])
        
        return relatedPassages

    def GetExpandedQuestion(self,question):
        tokens = nltk.word_tokenize(question.GetRawQuestion())
        new_tokens = []
        for token in tokens:
            #print("Token : "+token)
            if len(wn.synsets(token)) > 0:
                for syn in wn.synsets(token):
                    for lemma in syn.lemmas():
                        #print (lemma.name())
                        if(lemma.name().replace("_"," ") not in new_tokens):
                            new_tokens.append(lemma.name().replace("_"," "))
            else:
                if(token not in new_tokens):
                    new_tokens.append(token)
        return " ".join(new_tokens)