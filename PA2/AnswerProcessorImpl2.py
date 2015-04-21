import Utils
import AnswerTypeConvertor
from AnswerProcessor import IAnswerProcessor

''' Returns the cadidate answers just on the basis of expected answer type
    Actual processor used in the system should be more sophisticated
'''
class AnswerProcessorImpl2(IAnswerProcessor):
  
    def __GetAnswerType(self, question):
        return AnswerTypeConvertor.AnswerTypeToDescription(question.GetExpectedAnswerType())
    
    def GetAnswers(self, question, relevent_passages_and_scores, num_answers=10):
        candidate_answers = set()
        expected_answer_type = self.__GetAnswerType(question)
                
        for passage_and_score in relevent_passages_and_scores:
            tagged_list = Utils.TagNamedEntities(passage_and_score[0])
            for word_tag_pair in tagged_list:
                if word_tag_pair[1] == expected_answer_type:
                    candidate_answers.add(word_tag_pair[0])
                    if len(candidate_answers) >= num_answers:
                        break
        
        return list(candidate_answers)