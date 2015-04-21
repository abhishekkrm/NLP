import re
from nltk.tokenize import sent_tokenize

''' A class representing a document returned by IR system
'''
class Document(object):
    def __init__(self, document_data):
        self.__score = 0.0
        self.__rank = 0
        self.text = ''
        self.__passages = []
        self.__ParseDocument(document_data)
        
    def __ParseDocument(self, document_data):
        self.__PopulateRankAndScore(document_data)
        self.__PopulateText(document_data)
        self.__PopulatePassages(document_data)

    def __PopulateRankAndScore(self, document_data):
        rank_and_score = re.findall('Rank:.*Score:.*', document_data)
        self.__rank = int(re.findall('Rank: \d+', rank_and_score[0])[0].split(':')[1].strip())
        self.__score = float(re.findall('Score: \d*\.*\d+', rank_and_score[0])[0].split(':')[1].strip())
    
    def __Stringize(self, segment_list):
        result_text = ''
        for segment in segment_list:
            result_text += segment
        return result_text
    
    def __GetBodyText(self, document_data):
        
        result_text = self.__RemoveTag(self.__Stringize(self.__GetTagData(document_data, 'CAPTION')), 'CAPTION')
        result_text+= self.__RemoveTag(self.__Stringize(self.__GetTagData(document_data, 'HEADLINE')), 'HEADLINE')
        result_text+= self.__RemoveTag(self.__Stringize(self.__GetTagData(document_data, 'SUBJECT')), 'SUBJECT')
        result_text+= self.__RemoveTag(self.__Stringize(self.__GetTagData(document_data, 'GRAPHIC')), 'GRAPHIC')
        result_text+= self.__RemoveTag(self.__Stringize(self.__GetTagData(document_data, 'TEXT')), 'TEXT')
        result_text += self.__RemoveTag(self.__Stringize(self.__GetTagData(document_data, 'LEADPARA')), 'LEADPARA')
        return result_text
        
    def __PopulateText(self, document_data):
        text = self.__GetBodyText(document_data)
        self.__text = self.__RemoveTag(text, 'P')
           
    def __PopulatePassages(self, document_data):
        text = self.__GetBodyText(document_data)
        if ('<P>' in text) or ('<p>' in text):
            passages = self.__GetTagData(text, 'P')
            for passage in passages:
                refined_passage = self.__RemoveTag(passage, 'P').strip()
                if len(refined_passage) > 2:
                    self.__passages.append(refined_passage)
        else:
            passages = text.split('\n')
            for passage in passages:
                if len(passage.strip()) > 2:
                    self.__passages.append(passage.strip())
    
    def __GetTagData(self, document_data, tag):
        search_tag = '<' + tag + '.*?>.*?' + '</' + tag + '>'
        return re.findall(search_tag, document_data, re.DOTALL)
    
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
    
    def GetPassages(self):
        return self.__passages
    