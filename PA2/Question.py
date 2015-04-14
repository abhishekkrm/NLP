

''' A class representing a question.
'''
class Question(object):
    def __init__(self, question_no, raw_question):
        self.__question_number = question_no
        self.__raw_question = raw_question
        self.__keywords = []
        self.__expected_answer_types = []
        self.__top_documents = []
        
    def GetQuestionNumber(self):
        return self.__question_number
    
    def GetRawQuestion(self):
        return self.__raw_question
    
    def SetKeywords(self, keywords):
        self.__keywords = keywords
        
    def GetKeywords(self):
        return self.__keywords
    
    def SetExpectedAnswerTypes(self, expected_answer_types):
        self.__expected_answer_types = expected_answer_types
        
    def GetExpectedAnswerTypes(self):
        return self.__expected_answer_types
    
    def SetTopDocuments(self, top_documents):
        self.__top_documents = top_documents
        
    def GetTopDocuments(self):
        return self.__top_documents