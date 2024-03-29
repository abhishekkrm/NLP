import os
import re
import Document
import Utils
import MLQuestionProcessors
from Question import Question
from PassageRetrieverImpl1 import PassageRetrieverImpl1
from PassageRetrieverImpl2 import PassageRetrieverImpl2
from PassageRetrieverImpl3 import PassageRetrieverImpl3
from AnswerProcessorImpl1 import AnswerProcessorImpl1
from AnswerProcessorImpl2 import AnswerProcessorImpl2

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
    
    def __RetrieveReleventPassages(self, question, passage_retriever, num_passages):
        return passage_retriever.GetRelatedPassages(question, num_passages)
    
    def __ProcessAnswers(self, question, relevent_passages_and_scores, answer_processor, num_answers):
        return answer_processor.GetAnswers(question, relevent_passages_and_scores, num_answers)
    
    def GenerateAnswers(self, question_processor, passage_retrievers, answer_processor, ans_filename):
        answers = {}

        for _, question in self.__questions.items():
            print ('~~~~~~~~~~~~~~~~Question~~~~~~~~~~~~~~~~')
            
            self.__ProcessQuesion(question, question_processor)
            print("Question: "+ question.GetRawQuestion())
            print("AnswerType: " + question.GetExpectedAnswerType())
            print("Question Keywords: " + ' '.join(question.GetKeywords()))          
            for passage_retriever, num_passages, num_answers in passage_retrievers:
                relevent_passages_and_scores = self.__RetrieveReleventPassages(question, passage_retriever, num_passages)
                #print("--------------Relevant Passages --------------")
                #for passage_and_score in relevent_passages_and_scores:
                    #print(passage_and_score[0])
                self.__ProcessAnswers(question, relevent_passages_and_scores, answer_processor, num_answers)
            
            print('~~~~~~~~~~~~~~~~AnswerList~~~~~~~~~~~~~~~~')
            for answer in question.GetAnswerList():
                print(answer)
        
        #Let question processor save its information for speedup in next run
        question_processor.DumpInfo()
        
        #write answer file and evaluate using given script
        self._GenerateAnswerFile(ans_filename)
        self._ValidateAnswerFile(validation_script, answers_patterns_file, ans_filename)
                
        return answers
    
    ''' Generates the answer file in a format that evaluation script expects
    '''
    def _GenerateAnswerFile(self, ans_filename):
        with open(ans_filename, "w") as fp:
            for qid, question in self.__questions.items():
                answer_list = question.GetAnswerList()
                fp.write("qid "+ str(qid)+"\n")
                for i in range(0,len(answer_list)):
                    response_no = i+1
                    fp.write(str(response_no) + " " + str(answer_list[i]) + "\n")
    
    ''' Runs given evaluation.py on answer file 
    '''
    def _ValidateAnswerFile(self, eval_script, ans_pattern_file, ans_file):
        os.system("chmod +x \"" + eval_script + "\"")
        os.system("/usr/bin/python3.4 \"" + eval_script + "\" \"" + ans_pattern_file + "\" \"" + ans_file + "\"")
    
    ''' Get a question given the questionNo (for testing purposes)
    '''
    def _GetQuestion(self,questionNo):
        return self.__questions[questionNo]
   
    ''' Debugging support
    '''
    def __DebugGetQuestionProcessorPreClassifiedFile(self, question_processor_type):
        if question_processor_type.__name__ == 'MultinomialNBQuestionProcessor':
            return os.path.join(this_file_path, 'a_MultinomialNBQuestion.txt')
        elif question_processor_type.__name__ == 'LinearSVCQuestionProcessor':
            return os.path.join(this_file_path, 'a_LinearSVCQuestion.txt')
        elif question_processor_type.__name__ == 'DecisionTreeQuestionProcessor':
            return os.path.join(this_file_path, 'a_DecisionTreeQuestion.txt')
            
    ''' Debugging support
    '''
    def __DebugQuestionProcesssor(self, question, question_processor_type):
        classification_file = self.__DebugGetQuestionProcessorPreClassifiedFile(question_processor_type)
       
        with open(classification_file) as classification_fp:
            for line in classification_fp:
                ans_type_and_question = line.strip().split('~')
                if ans_type_and_question[1] == question.GetRawQuestion():
                    question.SetExpectedAnswerType(ans_type_and_question[0])
                    return
                
        #control should never reach here - unless there is a bug!
        assert False
        
    ''' As the name suggests for debugging purposes
    '''
    def _Debug(self, question_processor_type, passage_retrievers, answer_processor):
        for q_no in [2, 7, 8, 11, 15, 34, 39, 55, 63, 105, 31, 35]:
            question =  self._GetQuestion(q_no)
            
            print ('~~~~~~~~~~~~~~~~Question~~~~~~~~~~~~~~~~')
            self.__DebugQuestionProcesssor(question, question_processor_type)
            
            def GetQueryKeywords(question):
                listtag = {'NN','NNP','NNS','PRP','VBP','VBN','VBG','JJR','JJ','RB','FW'}
                text = question.GetRawQuestion()
                text = re.sub('\?', '', text)
                pos_tags = Utils.POSTag(text)
    
                result_keywords = [word_tag[0] for word_tag in pos_tags if word_tag[1] in listtag]
    
                if len(result_keywords) == 0:
                    result_keywords = Utils.RemoveStopwords(text).split()
    
                return result_keywords
            
            question.SetKeywords(GetQueryKeywords(question))
            
            print("Question: "+ question.GetRawQuestion())
            print("AnswerType: " + question.GetExpectedAnswerType())
            print("Keywords: " + ' '.join(question.GetKeywords()))
            
            for passage_retriever, num_passages, num_answers in passage_retrievers:
                relevent_passages_and_scores = self.__RetrieveReleventPassages(question, passage_retriever, num_passages)
                
                #print("--------------Relevant Passage And Scores --------------")
                #for passage_and_score in relevent_passages_and_scores:
                    #print(Utils.POSTag(Utils.RemoveStopwords(Utils.RemovePunctuation(passage_and_score[0]))))
                    #print(Utils.GetPhrases(Utils.RemoveStopwords(Utils.RemovePunctuation(passage_and_score[0]))))
                    #print(Utils.GetPhrases(Utils.RemoveStopwords(passage_and_score[0])))
                    
                self.__ProcessAnswers(question, relevent_passages_and_scores, answer_processor, num_answers)
            
            print('~~~~~~~~~~~~~~~~AnswerList~~~~~~~~~~~~~~~~')
            for answer in question.GetAnswerList():
                print(answer)
       
def main():
    controller = Controller(dev_questions_file, dev_top_docs_folder)

    # Can be LinearSVCQuestionProcessor or MultinomialNBQuestionProcessor or DecisionTreeQuestionProcessor
    question_processor = MLQuestionProcessors.LinearSVCQuestionProcessor(question_type_training_file_5500)
    
    # Can be PassageRetrieverImpl1 or PassageRetrieverImpl2 or PassageRetrieverImpl3
    passage_retriever_1 = PassageRetrieverImpl1()    
    passage_retriever_2 = PassageRetrieverImpl2()
    passage_retrievers = [(passage_retriever_2, 10, 3), (passage_retriever_1, 50, 10)]
    
    # Can be AnswerProcessorImpl1 or AnswerProcessorImpl2
    answer_processor = AnswerProcessorImpl1()
    
    # Generate Answer and write to answer_file
    controller.GenerateAnswers(question_processor, passage_retrievers, answer_processor,answer_file)
    
    #For debugging purposes
    #controller._Debug(MLQuestionProcessors.LinearSVCQuestionProcessor, passage_retrievers, answer_processor)
    

if __name__ == '__main__':
    main()
