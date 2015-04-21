import os
import Document
import Utils
import MLQuestionProcessors
from PassageRetrieverImpl1 import PassageRetrieverImpl1
from PassageRetrieverImpl2 import PassageRetrieverImpl2
from PassageRetrieverImpl3 import PassageRetrieverImpl3
from Question import Question
from AnswerProcessorImpl1 import AnswerProcessorImpl1
from AnswerProcessorImpl2 import AnswerProcessorImpl2
DEBUG = True


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
        return passage_retriever.GetRelatedPassages(question)
    
    def __ProcessAnswers(self, question, relevent_passages, answer_processor):
        return answer_processor.GetAnswers(question, relevent_passages)
    
    def GenerateAnswers(self, question_processor, passage_retriever, answer_processor, ans_filename):
        answers = {}

        for _, question in self.__questions.items():
            self.__ProcessQuesion(question, question_processor)
            if DEBUG:
                print("Question: "+ question.GetRawQuestion())
                print("AnswerType: " + question.GetExpectedAnswerType())
                print("Keywords: "+ " ".join(question.GetKeywords()))
            relevent_passages = self.__RetrieveReleventPassages(question, passage_retriever)
            if DEBUG:
                print("--------------RelevantPassage--------------")
                for p in relevent_passages:
                    print(p[0])
                    #print(Utils.TagNamedEntities(Utils.RemovePunctuation(p[0])))
                    #print(p[1])
                    pass
            candidate_answers = self.__ProcessAnswers(question, relevent_passages, answer_processor)
            if DEBUG:
                print('~~~~~~~~~~~~~~~~AnswerList~~~~~~~~~~~~~~~~')
                for ans in candidate_answers:
                    print (ans)
                print ('~~~~~~~~~~~~~~~~Question~~~~~~~~~~~~~~~~')
            question.SetAnswerList(candidate_answers)
            answers[question.GetQuestionNumber()] = candidate_answers
        
        #Let question processor save its information for speedup in next run
        question_processor.DumpInfo()
        self.__GenerateAnswerFile(ans_filename)
        return answers
    
    ''' Generates the answer file in a format that evaluation script expects
    '''
    def __GenerateAnswerFile(self, ans_filename):
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
        print("Training")
        mtqp = MLQuestionProcessors.MultinomialNBQuestionProcessor(question_type_training_file_1000)
        print("Passage Retreival")
        passage_retriever = PassageRetrieverImpl2()
        for _, question in self.__questions.items():
            question.SetExpectedAnswerType(mtqp.GetAnswerType(question))
            print(question.GetRawQuestion())
            print(question.GetExpectedAnswerType())
            print("--------------------------------")
            passageList = passage_retriever.GetRelatedPassages(question)
            for p in passageList:
                print (p[0])
                print (p[1])
            answer_p = AnswerProcessorImpl1()
            ansList = answer_p.GetAnswers(question, passageList, 20)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            for ans in ansList:
                print (ans)
            print ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            
        
def main():

    if DEBUG:
        print("Question and Answering System")
    controller = Controller(dev_questions_file, dev_top_docs_folder)

    # Can be LinearSVCQuestionProcessor or MultinomialNBQuestionProcessor or DecisionTreeQuestionProcessor
    question_processor = MLQuestionProcessors.MultinomialNBQuestionProcessor(question_type_training_file_1000)
    if DEBUG:
        print("Question Processor: " + question_processor.GetInfo())
  
    # Can be PassageRetrieverImpl1 or PassageRetrieverImpl2 or PassageRetrieverImpl3
    passage_retriever = PassageRetrieverImpl2()    
    if DEBUG:
        print("Passage Retreiver: " + passage_retriever.GetInfo())

    # Can be AnswerProcessorImpl1 or AnswerProcessorImpl2
    answer_processor = AnswerProcessorImpl1()
    if DEBUG:
        print("Answer Processor: " + answer_processor.GetInfo())
    
    if DEBUG:
        print("Generating Answers....")
        print("~~~~~~~~~~~~~~~~Question~~~~~~~~~~~~~~~~")
    # Generate Answer and write to answer_file
    controller.GenerateAnswers(question_processor, passage_retriever, answer_processor,answer_file)
  
    if DEBUG:
        print("Evaluating Answers.....")
    # Validation using Evaluation Script
    controller.ValidateAnswerFile(validation_script, answers_patterns_file, answer_file)
    
    # Debug Function
    # controller._Debug()

if __name__ == '__main__':
    main()
