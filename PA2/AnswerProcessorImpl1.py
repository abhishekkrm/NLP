import Utils
import itertools
import operator
from AnswerProcessor import IAnswerProcessor
from nltk.corpus import wordnet as wn

class AnswerProcessorImpl1(IAnswerProcessor):
    
    def __GetAnswerType(self, question):
        return question.GetExpectedAnswerType()
    
    def __ProcessText(self, text):
        return Utils.RemovePunctuation(text)
    
    def __IsAnswerTypeNERRecognizeable(self, answer_type):
        return True
    
    def __IsTokenInSynsets(self, token, expected_synsets):
        if len(wn.synsets(token)) > 0:
            search_synset = wn.synsets(token)[0]
            while True:
                if search_synset in expected_synsets:
                    return True
                if len(search_synset.hypernyms()) == 0:
                    break
                search_synset = search_synset.hypernyms()[0]
        return False
    
    def __GetAnswersUsingNER(self, question, relevent_passages, num_answers):
        candidate_answers = set()
        collected_candidate_answers = 0
        expected_answer_type = self.__GetAnswerType(question)
        
        for passage in relevent_passages:
            ner_tags = Utils.TagNamedEntities(self.__ProcessText(passage))
            
            for ner_tag , word_tag_group in itertools.groupby(ner_tags, key=operator.itemgetter(1)):
                if ner_tag == expected_answer_type:
                    candidate_answers.add(' '.join([word_tag[0] for word_tag in word_tag_group]))
                    collected_candidate_answers += 1
                    if collected_candidate_answers >= num_answers:
                        break
                    
        return list(candidate_answers)
    
    def __GetAnswersUsingWordNet(self, question, relevent_passages, num_answers):
        candidate_answers = set()
        collected_candidate_answers = 0
        expected_answer_synsets = wn.synsets(self.__GetAnswerType(question))
        
        if len(expected_answer_synsets) > 0:
            for passage in relevent_passages:
                for token in self.__ProcessText(passage).split():
                    if self.__IsTokenInSynsets(token, expected_answer_synsets):
                        candidate_answers.add(token)
                        collected_candidate_answers += 1
                        if collected_candidate_answers >= num_answers:
                            break
        
        return list(candidate_answers)
    
    def GetAnswers(self, question, relevent_passages, num_answers=10):
        if self.__IsAnswerTypeNERRecognizeable(self.__GetAnswerType(question)):
            return self.__GetAnswersUsingNER(question, relevent_passages, num_answers)
        else:
            return self.__GetAnswersUsingWordNet(question, relevent_passages, num_answers)
    