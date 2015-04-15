from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords


''' A class representing a document returned by IR system
'''
class Document(object):
    def __init__(self, document_data):
        self.__ParseDocument(document_data)
        
    def __ParseDocument(self, document_data):
        self.__score=float(document_data.split("Score: ")[-1].split("\n")[0])
        text=document_data.split("<TEXT>\n")[-1].split("\n</TEXT>")[0]
        # Remove <P> and </P> and \n
        text=text.replace("<P>\n","").replace("</P>\n","").replace("\n"," ").replace("  "," ")
        text=text.replace("<P>","").replace("</P>","")
        self.__text=text

    def GetScore(self):
        return self.__score

    def GetText(self):
        return self.__text

    ''' Remove the stopwords in text t and return new string
    '''
    def RemoveStopwords(self,t):
        stop = stopwords.words('english')
        return ' '.join([i for i in t.split() if i not in stop])

    ''' Returns a list of the sentences of the document
    '''
    def ParseSentences(self):
        sentences=sent_tokenize(self.__text)
        result=[]
        for s in sentences:
            if len(s)>2:
                result.append(s)
        return result

    ''' Returns a dictionary of Sentence->TF-IDF Similarity with the question
    '''
    def GetTFIDFSentenceRelevance(self,question):
        vect = TfidfVectorizer(min_df=1)
        sentences=self.ParseSentences()
        # Remove stop words from sentences and set to lowercase
        sentencesCleared=[]
        questionCleared=self.RemoveStopwords(question.GetRawQuestion().lower())       
        for s in sentences:
            sentencesCleared.append(self.RemoveStopwords(s).lower())
        # Compute the TFIDF similarity between the question and the sentences
        tfidf = vect.fit_transform([questionCleared]+sentencesCleared)
        score= (tfidf * tfidf.T).A[0,1:]
        sentenceRelevance={}		
        for i in range(len(sentencesCleared)):
            sentenceRelevance[sentences[i]]=score[i]
        return sentenceRelevance
      	
