import nltk
from nltk.corpus import stopwords
import abc
from abc import ABCMeta
from nltk.tag.stanford import NERTagger
import os.path
from collections import Counter

class IQuestionProcessor(metaclass=ABCMeta):
    
    ''' Given a question find out the important keywords in it.
        return a list of keywords
    '''
    @abc.abstractmethod
    def GetQueryKeywords(self, raw_question_text):
        pass
    
    ''' Given a question find out what answer type it expects (eg. PERSON, CITY ?)
        return a list of answer types (in rank order possibly ??)
    '''
    @abc.abstractmethod
    def GetAnswerType(self, question):
        pass

class DecisionTreeQuestionProcessor(IQuestionProcessor):
    __classifier = 0
    __st = NERTagger('/home/jai/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/jai/Downloads/stanford-ner-2014-06-16/stanford-ner.jar') # doctest: +SKIP
    __dict_set = set()
    __answer_dict = {}
    
    def GetQueryKeywords(self, question):
        tokens = nltk.word_tokenize(question.GetRawQuestion())
        ''' Following part is left commented to enable removal of stop words
        '''
        #stop = stopwords.words('english')
        #print("After removing stopwords")
        #new_tokens = []
        #for i in tokens:
        #    if(i not in stop):
        #        new_tokens.append(i)
        #print(new_tokens)
        return tokens
    
    def GenerateModel(self):
        
        if(os.path.exists('answer_types.txt') == True):
            with open('answer_types.txt') as f:
                lines = f.readlines()
            for line in lines:
                splt = line.split('~')
                self.__answer_dict[int(splt[0])] = splt[1]
            return
        
        featureset = []
        
        with open("qtype_train_1000.txt") as f:
            lines = f.readlines()
        
        
        for line in lines:
            #i = i+1
            #if(i>1000):
            #    break
            splt = line.split()[1:]
            temp = line.split()[0]
            sent = " ".join(splt)
            (trigrams,dict)= self.GetNGrams(sent)
            self.__dict_set |= set(trigrams)

        for line in lines:
            splt = line.split()[1:]
            temp = line.split()[0]
            sent = " ".join(splt)
            (line_ngrams,dict) = self.GetNGrams(sent)
            feature_dict = {}
            for f in self.__dict_set:
                if(f in line_ngrams):
                    feature_dict[" ".join(f)] = 1
                else:
                    feature_dict[" ".join(f)]=0
                
            featureset.append((feature_dict,temp))
        print(len(featureset))
        print("Training classifier")
        self.__classifier = nltk.classify.DecisionTreeClassifier.train(featureset, entropy_cutoff=0,support_cutoff=0)
    
    ''' Returns nGrams and n-gram counts
    '''
    def GetNGrams(self,sent):
        tokens = nltk.word_tokenize(sent)
        ''' Following part is left commented to use NER and POS tagging as features 
        '''
        #pos_tokens =[]
        #st = NERTagger('/home/jai/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/jai/Downloads/stanford-ner-2014-06-16/stanford-ner.jar') # doctest: +SKIP
        #print(self.__st.tag(tokens)[0])
        #for (token,pos) in nltk.pos_tag(tokens):
        #    pos_tokens.append(pos)
        ''' Using bigrams
        '''
        bigrams = nltk.ngrams(tokens, 2)
        list = set()
        dict = {}
        for ngram, count in Counter(bigrams).items():
            dict[' '.join(ngram)] = count
            list.add(ngram)
        return (list,dict)
    
    ''' Returns answer type of a given question
    '''
    def GetAnswerType(self, question):
        if(len(self.__answer_dict)>0):
            return self.__answer_dict[question.GetQuestionNumber()]
    
        raw_question_text = question.GetRawQuestion()
        tokens = self.GetQueryKeywords(question)
        print(raw_question_text)
        (line_ngrams,dict) = self.GetNGrams(raw_question_text)
        feature_dict = {}
        for f in self.__dict_set:
            if(f in line_ngrams):
                feature_dict[" ".join(f)] = 1
                #print(str(f)+" found in ngram")
            else:
                feature_dict[" ".join(f)] = 0
        #print(feature_dict)
        answer_type = self.__classifier.classify(feature_dict)
        #print(st.tag(tokens)) 
        #print(nltk.pos_tag(tokens))
        return answer_type
    
    