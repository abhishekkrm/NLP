import abc
import Utils
from abc import ABCMeta

class IAnswerProcessor(metaclass=ABCMeta):
    
    ''' Given a list of relevent passages, returns a list of N possible answers in ranked order.
    '''
    @abc.abstractmethod
    def GetAnswers(self, question, relevent_passages, num_answers=10):
        pass
    
class SimpleAnswerProcessor(IAnswerProcessor):
    ''' Returns the cadidate answers just on the basis of expected answer type
        Actual processor should be more sophisticated
    '''
    def GetAnswers(self, question, relevent_passages, num_answers=10):
        candidate_answers = []
        expected_answer_type = question.GetExpectedAnswerType()
        collected_candiate_answers = 0
        
        for passage in relevent_passages:
            tagged_list = Utils.TagNamedEntities(passage)
            for word_tag_pair in tagged_list:
                if word_tag_pair[1] == expected_answer_type:
                    candidate_answers.append(word_tag_pair[0])
                    collected_candiate_answers += 1
                    if collected_candiate_answers == num_answers:
                        break
        
        return candidate_answers
            