import os
import nltk
from nltk.corpus import stopwords
from nltk.tag.stanford import NERTagger
from nltk.util import ngrams

#constants
this_file_path = os.path.dirname(os.path.realpath(os.path.basename(__file__)))
stanford_ner_folder = os.path.join(this_file_path, 'stanford-ner-2015-01-30')

#Creating global - For optimization:
ner_jar_path = os.path.join(stanford_ner_folder, 'stanford-ner.jar')
ner_classifier_path = os.path.join(stanford_ner_folder, 'classifiers', 'english.all.7class.distsim.crf.ser.gz') 
ner_tagger = NERTagger(ner_classifier_path, ner_jar_path)
    

''' Remove the stopwords in the given text and return new string
'''
def RemoveStopwords(text):
    stopWordsList = stopwords.words('english')
    textWrods = text.split()
    return ' '.join([word for word in textWrods if word not in stopWordsList])
 
''' Given a list of words returns a list of tuples of type (word, NE tag)
'''
def TagNamedEntitiesInList(word_list):
    return ner_tagger.tag(word_list)

''' Given a text returns a list of tuples of type (word, NE tag)
'''
def TagNamedEntities(text):
    return TagNamedEntitiesInList(text.split())

''' Given a text returns a list of tuples of type (word, POS tag)
'''
def POSTag(text):
    tokens = text.split()
    return nltk.pos_tag(tokens)

''' Given a text returns a list of ngrams
'''
def GetNGrams(text, N = 2):
    return ngrams(text.split(), N)

