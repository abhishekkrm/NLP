

class Parser(object):
    def __init__(self, content_file, label = None):
        self.__list_of_mails = []
        self.__parse_file(content_file, label)
    
    def __parse_file(self, content_file, label):
        """ Should parse the content_file and read only mails makred by *label*
            If label is None, it should read every mail
        """
        pass
    
    def get_parsed_content(self):
        """Returns a string which contains all parsed mails concatenated.
        """
        return " ".join(self.__list_of_mails)
    
    def get_parsed_mails(self):
        """Returns a list of mails.
        """
        return self.__list_of_mails
    