import Utils
from QuestionProcessor import IQuestionProcessor
from nltk.corpus import wordnet as wn

class TREC9QuestionProcessor(IQuestionProcessor):

    ''' Given a question find out the important keywords in it.
        return a list of keywords
    '''
    def GetQueryKeywords(self, question):
        question_text_without_stop_words =  Utils.RemoveStopwords(question.GetRawQuestion())
        return question_text_without_stop_words.split()
    
    ''' Given a question find out what answer type it expects (eg. PERSON, CITY ?)
        return a list of answer types (in rank order possibly ??)
    '''
    def GetAnswerType(self, question):
        raw_question_text = question.GetRawQuestion()
        
        #When, where, why, describe, define
        straight_types = {  'When' : 'TIME',
                            'Where' : 'PLACE',
                            'Why' : 'REASON',
                            'Describe' : 'DESCRIPTION',
                            'Define' : 'DEFINITION'
                        }
        for question_word, ans_type in straight_types.items():
            if Utils.ContainsWholeWord(raw_question_text, question_word) == True:
                return ans_type
        
        #Who, Whom
        pos_tags = Utils.POSTag(raw_question_text)
        if Utils.ContainsWholeWord(raw_question_text, 'who') or Utils.ContainsWholeWord(raw_question_text, 'whom'):
            if len(pos_tags) > 2 and (pos_tags[0][0].lower()=='who' or pos_tags[0][0].lower()=='whom') \
                                 and (pos_tags[1][0].lower()=='is' or pos_tags[1][0].lower()=='are' or pos_tags[1][0].lower()=='was') \
                                 and (pos_tags[2][1] == 'NNP'):
                return 'DESCRIPTION'
            else:
                return 'PERSON' 
                    
        #What Which Name
        if  Utils.ContainsWholeWord(raw_question_text, 'what')\
            or Utils.ContainsWholeWord(raw_question_text, 'which')\
            or Utils.ContainsWholeWord(raw_question_text, 'name'):
           
            question_focus_set = Utils.GetPhrases(raw_question_text, 'NP')
            question_focus_synset = None
            question_focus = ''
            for focus in question_focus_set:
                if len(wn.synsets(focus)) > 0:
                    question_focus_synset = wn.synsets(focus)[0]
                    question_focus = focus
                    break
            
            if question_focus_synset:
                question_focus_hypoyms = question_focus_synset.hyponyms()
                person_synsets = wn.synsets('person')
                          
                for person_synset in person_synsets:
                    if person_synset in question_focus_hypoyms:
                        return 'PERSON'
                
                return question_focus
            else:
                return 'NAME'
        
        #how
        if Utils.ContainsWholeWord(raw_question_text, 'how'):
            question_words = raw_question_text.lower().split()
            word_follwing_how = question_words[question_words.index('how') + 1]
            
            if word_follwing_how == 'old':
                return 'AGE'
            elif word_follwing_how == 'many':
                return 'NUMBER'
            elif word_follwing_how == 'much':
                return 'QUANTITY'
            elif word_follwing_how == 'long':
                return 'DURATION'
            else:
                return 'MANNER'
        
        return 'UNKNOWN'
            
                   
            
        
        