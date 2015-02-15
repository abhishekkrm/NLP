

class Classifier(object):
    '''Constants for up and down mail classification'''
    UP_SPEAK = 1
    DOWN_SPEAK = 0
    
    def __init__(self, up_model, down_model):
        self.__up_model = up_model
        self.__down_model = down_model
        
    def classify_mail(self, unseen_mail):
        up_probability = self.__up_model.calculate_probability(unseen_mail)
        down_probability = self.__down_model.calculate_probability(unseen_mail)
        '''This may need to be improved later'''
        if up_probability > down_probability:
            return Classifier.UP_SPEAK 
        else:
            return Classifier.DOWN_SPEAK
        