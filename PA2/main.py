import os
from Question import *
from Document import *
from TFIDFPassageRetriever import *

this_file_path = os.path.realpath(os.path.basename(__file__))

answers_patterns_file = os.path.join('pa2-release', 'qadata', 'dev', 'answer_patterns.txt')
relevent_docs_file = os.path.join('pa2-release', 'qadata', 'dev', 'relevant_docs.txt')

dev_questions_file = os.path.join('pa2-release', 'qadata', 'dev','questions.txt')
test_questions_file = os.path.join('pa2-release', 'qadata', 'test','questions.txt')

dev_top_docs_folder = os.path.join('pa2-release', 'topdocs', 'dev')
test_top_docs_folder = os.path.join('pa2-release', 'topdocs', 'test')


class Controller(object):
    def __init__(self, questions_file, top_docs_folder):
        self.__questions = {} #A dictionary containing Question number <--> Question Objects
        self.__ParseQuestionsFile(questions_file)
        self.__ParseTopDocuments(top_docs_folder)
        
    ''' Read question number and raw question from file and create question object
    '''
    def __ParseQuestionsFile(self, questions_file):
    	i=0
        questionNumber=0
        with open(questions_file, "r") as ins:
            for line in ins:
	        if i%3==0:
	            questionNumber=int(line.rstrip("\r\n").lstrip("Number: "))	
	        if i%3==1:
                    self.__questions[questionNumber]=Question(questionNumber,line.rstrip("\r\n"))
                i+=1
    
    ''' Parses top documents and creates a list of Document objects for each Question Object 
    '''
    def __ParseTopDocuments(self, top_docs_folder):
        for questionNo in self.__questions:
            top_docs_file= os.path.join(top_docs_folder,"top_docs."+str(questionNo))
            text=""
            with open(top_docs_file, "r") as ins:
	        for line in ins:
		    text+=line
            splitDocuments=text.split("Qid: ") 
            del splitDocuments[0]
            top_documents=[]
            for textDocument in splitDocuments:
                document=Document(textDocument)
                top_documents.append(document)                               
            self.__questions[questionNo].SetTopDocuments(top_documents)
                
    def __ProcessQuesion(self, question, question_processor):
        pass
    
    def __RetrieveReleventPassages(self, question, passage_retriever):
        pass
    
    def __ProcessAnswers(self, question, relevent_passages, answer_processor):
        pass
    
    def GenerateAnswers(self, question_processor, passage_retriever, answer_processor):
        for _, question in self.__questions.items():
            self.__ProcessQuesion(question, question_processor)
            relevent_passages = self.__RetrieveReleventPassages(question, passage_retriever)
            candidate_answers = self.__ProcessAnswers(question, relevent_passages, answer_processor)

    ''' Get a question given the questionNo (for testing purposes)
    '''
    def GetQuestion(self,questionNo):
        return self.__questions[questionNo]
   
def main():
    controller = Controller(dev_questions_file, dev_top_docs_folder)
    passage_retriever= TFIDFPassageRetriever()

    ''' Code to test Related Passages
    question=controller.GetQuestion(10)
    print question.GetRawQuestion()
    relatedPassages=passage_retriever.GetRelatedPassages(question,10)
    for p in relatedPassages:
        print p
    '''
    #controller.GenerateAnswers(question_processor, passage_retriever, answer_processor)


if __name__ == '__main__':
    main()
