import Utils
import itertools
import operator
from AnswerProcessor import IAnswerProcessor

class AnswerProcessorImpl1(IAnswerProcessor):
    
    def __GetAnswerType(self, question):
        return question.GetExpectedAnswerType()
    
    def __ProcessText(self, text):
        return Utils.RemovePunctuation(text)
    
    def __IsAnswerTypeNERRecognizeable(self, answer_type):
        return True
    
    def __GetAnswersUsingNER(self, question, relevent_passages, num_answers):
        candidate_answers = []
        expected_answer_type = self.__GetAnswerType(question)
        
        for passage in relevent_passages:
            ner_tags = Utils.TagNamedEntities(self.__ProcessText(passage))
            
            for ner_tag , word_tag_group in itertools.groupby(ner_tags, key=operator.itemgetter(1)):
                if ner_tag == expected_answer_type:
                    candidate_answers.append(' '.join([word_tag[0] for word_tag in word_tag_group]))
       
        return candidate_answers[:num_answers]
    
    def __GetAnswersUsingWordNet(self, question, relevent_passages, num_answers):
        pass
    
    def GetAnswers(self, question, relevent_passages, num_answers=10):
        if self.__IsAnswerTypeNERRecognizeable(self.__GetAnswerType(question)):
            return self.__GetAnswersUsingNER(question, relevent_passages, num_answers)
        else:
            return self.__GetAnswersUsingWordNet(question, relevent_passages, num_answers)
    