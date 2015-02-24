from nltk.stem.snowball import SnowballStemmer
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
import NGramModel

class Parser(object):
    UP_LABEL = 'UPSPEAK'
    DOWN_LABEL = 'DOWNSPEAK'
    
    def __init__(self, content_file, label = None, remove_punctuation = True, lowercase = True, use_stemmer = False, use_lemmetizer = False):
        self.__list_of_mails = []
        self.__lowercase = lowercase
        self.__use_stemmer = use_stemmer
        self.__use_lemmetizer = use_lemmetizer
        if remove_punctuation:
            self.__tokenizer = RegexpTokenizer(r'\w+').tokenize
        else:
            self.__tokenizer = tokenize.wordpunct_tokenize
        self.__parse_file(content_file, label)

    def __parse_file(self, content_file, label):
        """ Should parse the content_file and read only mails makred by *label*
            If label is None, it should read every mail
        """
        with open(content_file) as f:
            lines = f.readlines()
            currentEmail=""
            toBeParsed=False
            for currentLine in lines:
                currentLine = currentLine.strip()
                if currentLine == Parser.UP_LABEL or currentLine == Parser.DOWN_LABEL:
                    if currentLine == label:
                        toBeParsed=True
                        continue	
                if currentLine=='**START**':
                    currentEmail=""
                elif currentLine=='**EOM**':
                    if toBeParsed or label == None:
                        self.__list_of_mails.append(self.__parse_email(currentEmail))
                    toBeParsed=False
                else:
                    currentEmail+=currentLine

    def __parse_email(self, email):
        if self.__lowercase:
            email = email.lower()
        sentences = tokenize.sent_tokenize(email)
        parsed_mail = []
        for sentence in sentences:
            tokens = self.__tokenizer(sentence)
            if self.__use_lemmetizer:
                tokens = [SnowballStemmer("english").stem(token) for token in tokens]
            elif self.__use_stemmer:
                tokens = [SnowballStemmer("porter").stem(token) for token in tokens]
            if len(tokens) > 0:
                self.__add_start_end_sentence_token(tokens)
                parsed_mail = parsed_mail + tokens
        return ' '.join(parsed_mail)
        
    def __add_start_end_sentence_token(self, tokens):
        tokens.insert(0, NGramModel.NGramModel.START_SENTENCE_TOKEN)
        tokens.append(NGramModel.NGramModel.END_SENTENCE_TOKEN)
    
    def get_parsed_content(self):
        """Returns a string which contains all parsed mails concatenated.
        """
        return " ".join(self.__list_of_mails)
    
    def get_parsed_mails(self):
        """Returns a list of mails.
        """
        return self.__list_of_mails

