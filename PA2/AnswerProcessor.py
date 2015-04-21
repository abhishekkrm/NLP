import abc
import Utils
from abc import ABCMeta
from gi.overrides.keysyms import question
from nltk.tokenize import RegexpTokenizer

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

''' NER based Answer processor
'''
class NERAnswerProcessor(IAnswerProcessor):
    ''' Returns list of (word,NER) tuples
    '''
    def GetAnswers(self,question,relevant_passages,num_answers=10):
         candidate_answers = []
         tokenizer = RegexpTokenizer(r'\w+')
         for passage in relevant_passages:
             tokens = tokenizer.tokenize(passage)
             tagged = Utils.TagNamedEntities(" ".join(tokens))
             prev_tag =""
             candidate =""
             iter = 0;
             #print(tagged[0])
             for (word,tag) in tagged[0]:
                 if(tag!='O'):
                     if(tag==prev_tag or prev_tag=='O' or iter==0):
                         candidate+=" "+word
                     else:
                         candidate+=word
                         #print(candidate.strip())
                         candidate_answers.append((candidate.strip(),prev_tag))
                         candidate=""
                 else:
                     if(candidate.strip()!=""):
                         #print(candidate.strip())
                         candidate_answers.append((candidate.strip(),prev_tag))
                         candidate=""
                     candidate=""
                 iter=iter+1
                 prev_tag = tag  
             if(candidate.strip()!=""):
                 #print(candidate.strip())
                 candidate_answers.append((candidate.strip(),prev_tag))
                 candidate=""
         print(candidate_answers)
         return candidate_answers  
                 