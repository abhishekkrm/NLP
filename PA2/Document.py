

''' A class representing a document returned by IR system
'''
class Document(object):
    def __init__(self, document_data):
        self.__ParseDocument(document_data)
        
    def __ParseDocument(self, document_data):
        self.score=float(document_data.split("Score: ")[-1].split("\n")[0])
        self.text=document_data.split("<TEXT>\n")[-1].split("\n</TEXT>")[0]
        # Remove <P> and </P> and \n
        self.text=self.text.replace("<P>\n","").replace("</P>\n","").replace("\n"," ").replace("  "," ")
        self.text=self.text.replace("<P>","").replace("</P>","")
      	
