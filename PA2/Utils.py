from nltk.corpus import stopwords

''' Remove the stopwords in the given text and return new string
'''
def RemoveStopwords(self, text):
    stopWordsList = stopwords.words('english')
    textWrods = text.split().strip()
    return ' '.join([word for word in textWrods if word not in stopWordsList])