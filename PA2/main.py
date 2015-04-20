import os
import nltk
import Document
import Utils
from Question import *
from TFIDFPassageRetriever import TFIDFPassageRetriever
import LanguageModel


this_file_path = os.path.dirname(os.path.realpath(os.path.basename(__file__)))

answers_patterns_file = os.path.join(this_file_path, 'pa2-release', 'qadata', 'dev', 'answer_patterns.txt')
relevent_docs_file = os.path.join(this_file_path, 'pa2-release', 'qadata', 'dev', 'relevant_docs.txt')

dev_questions_file = os.path.join(this_file_path, 'pa2-release', 'qadata', 'dev','questions.txt')
test_questions_file = os.path.join(this_file_path, 'pa2-release', 'qadata', 'test','questions.txt')

dev_top_docs_folder = os.path.join(this_file_path, 'pa2-release', 'topdocs', 'dev')
test_top_docs_folder = os.path.join(this_file_path, 'pa2-release', 'topdocs', 'test')

validation_script = os.path.join(this_file_path,'pa2-release','evaluation.py')
answer_file = os.path.join(this_file_path,'answer.txt')

class Controller(object):
    def __init__(self, questions_file, top_docs_folder):
        self.__questions = {} #A dictionary containing Question number <--> Question Objects
        self.__ParseQuestionsFile(questions_file)
        self.__ParseTopDocuments(top_docs_folder)
        self.__answers = {} #A dictionary containg Answer number <-->Answer Objects
        
    ''' Read question number and raw question from file and create question object
    '''
    def __ParseQuestionsFile(self, questions_file):
        with open(questions_file, "r") as ins:
            for line in ins:
                if line.strip() != '':
                    if line.startswith('Number:'):
                        questionNumber = int(line.split(':')[1].strip())
                    else:
                        self.__questions[questionNumber] = Question(questionNumber, line.strip())
    
    ''' Parses top documents and creates a list of Document objects for each Question Object 
    '''
    def __ParseTopDocuments(self, top_docs_folder):
        for questionNo in self.__questions:
            top_docs_file = os.path.join(top_docs_folder,"top_docs." + str(questionNo))
            
            text=""
            with open(top_docs_file, "r", errors='ignore') as ins:
                for line in ins:
                    text += line
            
            splitDocuments=text.strip().split("Qid: ") 
            del splitDocuments[0]
            #print(splitDocuments)
            #sleep(1)
            top_documents=[]
            for textDocument in splitDocuments:
                document = Document.Document(textDocument)
                top_documents.append(document)                               
            
            self.__questions[questionNo].SetTopDocuments(top_documents)
                
    def __ProcessQuesion(self, question, question_processor):
        pass
    
    def __RetrieveReleventPassages(self, question, passage_retriever):
        pass
    
    def __ProcessAnswers(self, question, relevent_passages, answer_processor):
        pass
    
    def GenerateAnswers(self, question_processor, passage_retriever, answer_processor):
        answers = {}
        for _, question in self.__questions.items():
            self.__ProcessQuesion(question, question_processor)
            relevent_passages = self.__RetrieveReleventPassages(question, passage_retriever)
            candidate_answers = self.__ProcessAnswers(question, relevent_passages, answer_processor)
            answers[question.GetQuestionNumber()] = candidate_answers
        return answers
    
    def GenerateAnswerFile(self, ans_filename):
        fp = open(ans_filename, "w")
        for qid, question in self.__questions.items():
            answer_list = question.GetAnswerList()
            fp.write("qid "+ str(qid)+"\n")
            for i in range(0,len(answer_list)):
                response_no = i+1
                fp.write(str(response_no) + " " + str(answer_list[i]) + "\n")

    def ValidateAnswerFile(self, eval_script, ans_pattern_file, ans_file):
        os.system("chmod +x " + eval_script)
        os.system("/usr/bin/python3.4 " + eval_script + " " + ans_pattern_file + " " + ans_file)
    
    ''' Get a question given the questionNo (for testing purposes)
    '''
    def _GetQuestion(self,questionNo):
        return self.__questions[questionNo]
   
    def _Debug(self):
        for _, question in self.__questions.items():
            #print(Utils.TagNamedEntities(question.GetRawQuestion()))
            #print("START---------------------------------------------------------------------")
            #question = self._GetQuestion(7)
            #answertag = LanguageModel.LanguageModel()
            #print(question.GetRawQuestion())
            #print(answertag.GetKeyWordsList(question.GetRawQuestion()))
            #print(answertag.GetAnswerTag(question.GetRawQuestion()))
            passage_retriever= TFIDFPassageRetriever()
            relatedPassages=passage_retriever.GetRelatedPassages(question,100)
            test = "All selections are served with sausage Italian herb potatoes and pandoro, a sweet Italian bread"
            print (Utils.TagNamedEntities(test))
            for p in relatedPassages:
#                print (p)
                text_type_list_passages = Utils.TagNamedEntities(p)
                for text_type_list in text_type_list_passages:
                    for text_type in text_type_list: 
                        #print (text_type)
                        #print ("----------")
                        text = text_type[0]
                        type = text_type[1]
                        if type != 'O':
                            print(str(text) +"-------->"+ str(type))
                            pass
            #print("END-------------------------------------------------------------------------------")
    #    print(p)
        
def main():
    controller = Controller(dev_questions_file, dev_top_docs_folder)
    #controller.GenerateAnswers(question_processor, passage_retriever, answer_processor)
    
    passage_retriever= TFIDFPassageRetriever()
 
    ''' Code to test Related Passages '''
    
    #controller._Debug()
    
    #relatedPassages=passage_retriever.GetRelatedPassages(question,20)
    #for p in relatedPassages:
    #    print(p)
    # Generate Answer File
    # controller.GenerateAnswerFile(answer_file)
    # Validation of Answer
    #controller.ValidateAnswerFile(validation_script, answers_patterns_file, answer_file)   


    
if __name__ == '__main__':
    main()
