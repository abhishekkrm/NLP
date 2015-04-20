import nltk
from QuestionProcessor import IQuestionProcessor
import Utils

class LanguageModel(IQuestionProcessor):
    def GetQueryKeywords(self, raw_question_text):
        pass
 
    def GetAnswerType(self, raw_question_text):
        pass
 
    def GetAnswerTag(self, text, listtag={'WP','WRB','NNP'}):
        tag_index = 1
        found = 0
        text_tag_list = nltk.pos_tag(nltk.word_tokenize(text))
        #print (text_tag_list)
        for text_tag in text_tag_list:
            if text_tag[tag_index] in listtag:
                #print(text_tag[text_index])
                found =1
        if found == 0:
            print (text_tag_list)
        pass
#     Taken from https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
#     1.    CC    Coordinating conjunction
#     2.    CD    Cardinal number
#     3.    DT    Determiner
#     4.    EX    Existential there
#     5.    FW    Foreign word
#     6.    IN    Preposition or subordinating conjunction
#     7.    JJ    Adjective
#     8.    JJR    Adjective, comparative
#     9.    JJS    Adjective, superlative
#     10.    LS    List item marker
#     11.    MD    Modal
#     12.    NN    Noun, singular or mass
#     13.    NNS    Noun, plural
#     14.    NNP    Proper noun, singular
#     15.    NNPS    Proper noun, plural
#     16.    PDT    Predeterminer
#     17.    POS    Possessive ending
#     18.    PRP    Personal pronoun
#     19.    PRP$    Possessive pronoun
#     20.    RB    Adverb
#     21.    RBR    Adverb, comparative
#     22.    RBS    Adverb, superlative
#     23.    RP    Particle
#     24.    SYM    Symbol
#     25.    TO    to
#     26.    UH    Interjection
#     27.    VB    Verb, base form
#     28.    VBD    Verb, past tense
#     29.    VBG    Verb, gerund or present participle
#     30.    VBN    Verb, past participle
#     31.    VBP    Verb, non-3rd person singular present
#     32.    VBZ    Verb, 3rd person singular present
#     33.    WDT    Wh-determiner
#     34.    WP    Wh-pronoun
#     35.    WP$    Possessive wh-pronoun
#     36.    WRB    Wh-adverb
    def GetKeyWordsList(self,text, listtag={'NN','NNP','NNS','PRP','VBP','VBN','VBG','JJR','JJ','RB','FW'}):
        tag_index = 1
        text_index = 0
        text_tag_list = nltk.pos_tag(nltk.word_tokenize(text))
        # print (text_tag_list)
        result_keywords = []
        for text_tag in text_tag_list:
            if text_tag[tag_index] in listtag:
                result_keywords.append(text_tag[text_index])
        if not result_keywords:
            result_keywords = Utils.RemoveStopwords(text).split()
        # print(result_keywords)
        return result_keywords
