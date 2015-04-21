import nltk
import operator
import Utils
from nltk.corpus import wordnet as wn
from PassageRetriever import IPassageRetriever
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PassageRetrieverImpl1(IPassageRetriever):
    
    def __ExpandQuestion(self, question_text):
        tokens = nltk.word_tokenize(question_text)
        new_tokens = set()
        
        for token in tokens:
            if len(wn.synsets(token)) > 0:
                for lemma in wn.synsets(token)[0].lemmas():
                    new_tokens |= set(lemma.name().split('_'))
            new_tokens.add(token)
        
        return ' '.join(new_tokens)
    
    def __ProcessText(self, text):
        return Utils.Lemmatize(Utils.RemoveStopwords(text.lower()))
    
    ''' From the list of top documents figures out the n most relevent passages
    '''                           
    def GetRelatedPassages(self, question, n = 10):
        processed_corpus = []
        processed_to_original_sentence_mapping = {}
        
        expended_question_text = self.__ExpandQuestion(self.__ProcessText(question.GetRawQuestion()))
        processed_corpus.append(expended_question_text)
        
        for document in question.GetTopDocuments():
            for sentence in document.GetSentences():
                processed_sentence = self.__ProcessText(sentence)
                processed_corpus.append(processed_sentence)
                processed_to_original_sentence_mapping[processed_sentence] = sentence
                
        #calculate TFIDF similarity
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(processed_corpus)
               
        similarity_scores = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train[1:])
        sim_score_processed_sentence_sorted = sorted(zip(similarity_scores[0], processed_corpus[1:]), key=operator.itemgetter(0), reverse=True)
        
        relevent_passages = [(processed_to_original_sentence_mapping[score_sentence[1]], score_sentence[0]) for score_sentence in sim_score_processed_sentence_sorted]
        return relevent_passages[:n]
