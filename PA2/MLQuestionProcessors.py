import Utils
import abc
from QuestionProcessor import IQuestionProcessor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB

class MLQuestionProcessorBase(IQuestionProcessor):
    def __init__(self, training_file, N_Gram_Range = (2,3)):
        self.__classifier = self.GetClassifier()
        self.__count_vectorizer = CountVectorizer(ngram_range=N_Gram_Range)
        self.__TrainClassifier(training_file)
    
    def __TrainClassifier(self, training_file):
        questions = []
        answer_types = []
        
        with open(training_file) as t_file:
            for label_question in t_file:
                answer_types.append(label_question.strip().split()[0])
                questions.append(' '.join(label_question.strip().split()[1:]))
        
        question_vectors = self.__count_vectorizer.fit_transform(questions).toarray()
        self.__classifier.fit(question_vectors, answer_types)
    
    def GetAnswerType(self, question):
        question_vector = self.__count_vectorizer.transform([question.GetRawQuestion()]).toarray()
        return self.__classifier.predict(question_vector)[0]
    
    def GetQueryKeywords(self, question):
        question_text_without_stop_words =  Utils.RemoveStopwords(question.GetRawQuestion())
        return question_text_without_stop_words.split()
    
    @abc.abstractmethod
    def GetClassifier(self):
        pass

    @abc.abstractmethod
    def GetInfo(self):
        pass
    
''' Linear Support Vector Classification
'''    
class LinearSVCQuestionProcessor(MLQuestionProcessorBase):
    def GetClassifier(self):
        return LinearSVC()
    
    def GetInfo(self):
        return self.__class__.__name__

''' Multinomial Naive Bayes Classifier
'''
class MultinomialNBQuestionProcessor(MLQuestionProcessorBase):
    def GetClassifier(self):
        return MultinomialNB()
    
    def GetInfo(self):
        return self.__class__.__name__

    def GetQueryKeywords(self, question, listtag={'NN','NNP','NNS','PRP','VBP','VBN','VBG','JJR','JJ','RB','FW'}):
        text = question.GetRawQuestion()
        pos_tags = Utils.POSTag(text)
        result_keywords = [word_tag[0] for word_tag in pos_tags if word_tag[1] in listtag]
        if len(result_keywords) == 0:
            result_keywords = Utils.RemoveStopwords(text).split()
        return result_keywords

''' Decision Tree Classifier
'''
class DecisionTreeQuestionProcessor(MLQuestionProcessorBase):
    def GetClassifier(self):
        return DecisionTreeClassifier()
    
    def GetInfo(self):
        return self.__class__.__name__
    