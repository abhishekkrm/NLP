

''' A class representing a question.
'''
class Question(object):
    def __init__(self, question_no, raw_question):
        self.__question_number = question_no
        self.__raw_question = raw_question
        self.__keywords = []
        self.__noun_phrases = []
        self.__expected_answer_type = ''
        self.__top_documents = []
        self.__answer_list = []
        
    def GetQuestionNumber(self):
        return self.__question_number
    
    def GetRawQuestion(self):
        return self.__raw_question
    
    def SetAnswerList(self, answerList):
        self.__answer_list = answerList
    
    def GetAnswerList(self):
        return self.__answer_list
        
    def SetKeywords(self, keywords):
        self.__keywords = keywords
        
    def GetKeywords(self):
        return self.__keywords
    
    def SetNounPhrases(self, noun_phrases):
        self.__noun_phrases = noun_phrases
        
    def GetNounPhrases(self):
        return self.__noun_phrases
    
    def SetExpectedAnswerType(self, expected_answer_type):
        self.__expected_answer_type = expected_answer_type
        
    def GetExpectedAnswerType(self):
        return self.__expected_answer_type
    
    def SetTopDocuments(self, top_documents):
        self.__top_documents = top_documents
        
    def GetTopDocuments(self):
        return self.__top_documents