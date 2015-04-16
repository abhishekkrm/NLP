import os
from nltk.corpus import stopwords
from nltk.tag.stanford import NERTagger

#constants
this_file_path = os.path.dirname(os.path.realpath(os.path.basename(__file__)))
stanford_ner_folder = os.path.join(this_file_path, 'stanford-ner-2015-01-30')

''' Remove the stopwords in the given text and return new string
'''
def RemoveStopwords(text):
    stopWordsList = stopwords.words('english')
    textWrods = text.split()
    return ' '.join([word for word in textWrods if word not in stopWordsList])
 
''' Given a list of words returns a list of tuples of type (word, NE tag)
'''
def TagNamedEntitiesInList(word_list):
    ner_jar = os.path.join(stanford_ner_folder, 'stanford-ner.jar')
    ner_classifier = os.path.join(stanford_ner_folder, 'classifiers', 'english.all.7class.distsim.crf.ser.gz') 
    
    tagger = NERTagger(ner_classifier, ner_jar)
    return tagger.tag(word_list)

''' Given a text returns a list of tuples of type (word, NE tag)
'''
def TagNamedEntities(text):
    return TagNamedEntitiesInList(text.split())
