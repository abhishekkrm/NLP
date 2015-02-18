def parseEmail(content,lowerCase=True,removePunctuation=True,removeNewline=True):
    """ Turns the content of an email into a tokenized sentences of the form:
	<s> a tokenized sentence (possibly a non-sentence) </s> <s> a tokenized sentence (possibly a non-sentence) </s>
    """
    content = content.strip();
    splt = content.split(". ");
    str = "";
    for i in range(0,len(splt)):
        if bool(splt[i].strip()):
            str+=" <s> "+splt[i].strip()+" </s>"
            'print(splt[i].strip())'
    if removeNewline:
        str=str.replace("\n"," ")
    if lowerCase:
        str=str.lower()
    if removePunctuation:
        str=str.replace(",","")
        str=str.replace(";","")
        str=str.replace("!","")	
        str=str.replace("?","")
        str=str.replace("\"","")
        str=str.replace("(","")
        str=str.replace(")","")
    # Remove tabs
    str=str.replace("\t"," ")
    # Remove double and triple spaces
    str=str.replace("  "," ")
    str=str.replace("  "," ")
    return str;

class Parser(object):
    def __init__(self, content_file, label = None):
        self.__list_of_mails = []
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
                if currentLine[:-1]==label or label==None:
                        toBeParsed=True	
                elif currentLine=='**START**\n':
                        currentEmail=""
                elif currentLine=='**EOM**\n':
                        if toBeParsed:
                            self.__list_of_mails.append(parseEmail(currentEmail))
                        toBeParsed=False
                else:
                        currentEmail+=currentLine

        pass
    
    def get_parsed_content(self):
        """Returns a string which contains all parsed mails concatenated.
        """
        return "".join(self.__list_of_mails)
    
    def get_parsed_mails(self):
        """Returns a list of mails.
        """
        return self.__list_of_mails


    
