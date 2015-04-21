import os
import nltk
import re
from nltk.corpus import stopwords
from nltk.tag.stanford import NERTagger
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

#constants
this_file_path = os.path.dirname(os.path.realpath(os.path.basename(__file__)))
stanford_ner_folder = os.path.join(this_file_path, 'stanford-ner-2015-01-30')

#Creating global - For optimization:
ner_jar_path = os.path.join(stanford_ner_folder, 'stanford-ner.jar')
ner_classifier_path = os.path.join(stanford_ner_folder, 'classifiers', 'english.all.7class.distsim.crf.ser.gz') 
ner_tagger = NERTagger(ner_classifier_path, ner_jar_path)

#Taken from https://gist.github.com/alexbowe/879414 
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)

''' Remove the stopwords in the given text and return new string
'''
def RemoveStopwords(text):
    stopWordsList = stopwords.words('english')
    textWrods = text.split()
    return ' '.join([word for word in textWrods if word not in stopWordsList])

''' Given a text returns a lemmetized string
'''
def Lemmatize(text):
    lmtzr = WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    return " ".join([lmtzr.lemmatize(token) for token in tokens])

''' Removes punctuation from given text
'''
def RemovePunctuation(text):
    tokenizer = RegexpTokenizer(r'\w+')
    return ' '.join(tokenizer.tokenize(text))
    
''' Given a list of words returns a list of tuples of type (word, NE tag)
'''
def TagNamedEntitiesInList(word_list):
    return ner_tagger.tag(word_list)[0]

''' Given a text returns a list of tuples of type (word, NE tag)
'''
def TagNamedEntities(text):
    return TagNamedEntitiesInList(nltk.word_tokenize(text))

''' Given a text returns a list of tuples of type (word, POS tag)
'''
def POSTag(text):
    tokens = nltk.word_tokenize(text)
    return nltk.pos_tag(tokens)

''' Given a text returns a list of ngrams
'''
def GetNGrams(text, N = 2):
    computed_ngrams = ngrams(text.split(), N)
    return [' '.join(ngram).strip() for ngram in computed_ngrams]

''' Given a text returns a dict of ngram counts. <ngram> <--> <count>
'''
def GetNGramCounts(text, N = 2):
    n_grams_text = GetNGrams(text, N)
    return dict((ngram, n_grams_text.count(ngram)) for ngram in n_grams_text)

''' Given text returns the list of specified Phrase (eg. NP for noun phrases) in it
'''
def GetPhrases(text, phrase='NP'):
    pos_tokens = POSTag(text)
    parse_tree = chunker.parse(pos_tokens)
    
    result_phrases = []
    for subtree in parse_tree.subtrees(filter=lambda t: t.label() == phrase):
        result_phrases.append(' '.join([ word[0] for word in subtree.leaves()]))
    return result_phrases
    
''' Return True if search_word exists as a word in text, False otherwise
    eg. text = "It was good show." search_word = "how" ==> Result: False
        text = "How are you?" search_word = "how" ==> Result =: True
'''    
def ContainsWholeWord(text, search_word):
    match_object = re.compile(r'\b({0})\b'.format(search_word), re.IGNORECASE).search(text)
    return match_object != None
