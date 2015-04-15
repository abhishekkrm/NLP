import re
from nltk.tokenize import sent_tokenize

''' A class representing a document returned by IR system
'''
class Document(object):
    def __init__(self, document_data):
        self.__score = 0.0
        self.__rank = 0
        self.text = ''
        self.__ParseDocument(document_data)
        
    def __ParseDocument(self, document_data):
        self.__PopulateRankAndScore(document_data)
        self.__PopulateText(document_data)

    def __PopulateRankAndScore(self, document_data):
        rank_and_score = re.findall('Rank:.*Score:.*', document_data)
        self.__rank = int(re.findall('Rank: \d+', rank_and_score[0])[0].split(':')[1].strip())
        self.__score = float(re.findall('Score: \d*\.*\d+', rank_and_score[0])[0].split(':')[1].strip())
    
    def __PopulateText(self, document_data):
        text = self.__GetTagData(document_data, 'TEXT')
        text += self.__GetTagData(document_data, 'LEADPARA')
        self.__text = self.__RemoveTag(text, 'P')
           
    def __GetTagData(self, document_data, tag):
        search_tag = '<' + tag + '.*?>.*?' + '</' + tag + '>'
        result_text = re.findall(search_tag, document_data, re.DOTALL)
        if len(result_text) > 0:
            return self.__RemoveTag(result_text[0], tag)
        else:
            return ''
    
    def __RemoveTag(self, data, tag):
        start_tag = '<' + tag + '.*?>'
        end_tag = '</' + tag + '>'
        
        result_text = re.sub(start_tag, '', data)
        result_text = re.sub(end_tag, '', result_text)
        
        return result_text
    
    def GetScore(self):
        return self.__score

    def GetText(self):
        return self.__text

    def GetRank(self):
        return self.__rank
    
    ''' Returns a list of the sentences of the document
    '''
    def GetSentences(self):
        sentences = sent_tokenize(self.__text)
        return [sentence for sentence in sentences if len(sentence) > 2]
