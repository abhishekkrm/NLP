import os
import Document
import Utils
import MLQuestionProcessors
from Question import Question

this_file_path = os.path.dirname(os.path.realpath(os.path.basename(__file__)))

answers_patterns_file = os.path.join(this_file_path, 'pa2-release', 'qadata', 'dev', 'answer_patterns.txt')
relevent_docs_file = os.path.join(this_file_path, 'pa2-release', 'qadata', 'dev', 'relevant_docs.txt')

dev_questions_file = os.path.join(this_file_path, 'pa2-release', 'qadata', 'dev','questions.txt')
test_questions_file = os.path.join(this_file_path, 'pa2-release', 'qadata', 'test','questions.txt')

dev_top_docs_folder = os.path.join(this_file_path, 'pa2-release', 'topdocs', 'dev')
test_top_docs_folder = os.path.join(this_file_path, 'pa2-release', 'topdocs', 'test')

question_type_training_file_1000 = os.path.join(this_file_path, 'qtype_train_1000.txt')
question_type_training_file_5500 = os.path.join(this_file_path, 'qtype_train_5500.txt')

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

            top_documents=[]
            for textDocument in splitDocuments:
                document = Document.Document(textDocument)
                top_documents.append(document)                               
            
            self.__questions[questionNo].SetTopDocuments(top_documents)
                
    def __ProcessQuesion(self, question, question_processor):
        question.SetNounPhrases(Utils.GetPhrases(question.GetRawQuestion(), 'NP'))
        question.SetKeywords(question_processor.GetQueryKeywords(question))
        question.SetExpectedAnswerType(question_processor.GetAnswerType(question))
    
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
        
        #Let question processor save its information for speedup in next run
        question_processor.DumpInfo()
        
        return answers
    
    ''' Generates the answer file in a format that evaluation script expects
    '''
    def GenerateAnswerFile(self, ans_filename):
        with open(ans_filename, "w") as fp:
            for qid, question in self.__questions.items():
                answer_list = question.GetAnswerList()
                fp.write("qid "+ str(qid)+"\n")
                for i in range(0,len(answer_list)):
                    response_no = i+1
                    fp.write(str(response_no) + " " + str(answer_list[i]) + "\n")
    
    ''' Runs given evaluation.py on answer file 
    '''
    def ValidateAnswerFile(self, eval_script, ans_pattern_file, ans_file):
        os.system("chmod +x " + eval_script)
        os.system("/usr/bin/python3.4 " + eval_script + " " + ans_pattern_file + " " + ans_file)
    
    ''' Get a question given the questionNo (for testing purposes)
    '''
    def _GetQuestion(self,questionNo):
        return self.__questions[questionNo]
   
    ''' As the name suggests for debugging purposes
    '''
    def _Debug(self):
        dtqp = MLQuestionProcessors.DecisionTreeQuestionProcessor(question_type_training_file_5500)
        for _, question in self.__questions.items():
            print(dtqp.GetAnswerType(question) + '~' + question.GetRawQuestion())
        dtqp.DumpInfo()
        
def main():
    controller = Controller(dev_questions_file, dev_top_docs_folder)
    #controller.GenerateAnswers(question_processor, passage_retriever, answer_processor)
    controller._Debug()

if __name__ == '__main__':
    main()
