

''' A class representing a document returned by IR system
'''
class Document(object):
    def __init__(self, document_file):
        self.__ParseDocumentFile(document_file)
        
    def __ParseDocumentFile(self, document_file):
        pass