import operator

class Sentence:
    def __init__(self, senctence):
        self.sentence = senctence
        self.rhyme = 'null'


    # Getery
    def get_sentence(self):
        return self.sentence

    def get_rhyme(self):
        return self.rhyme

    # Setery
    def add_sentence(self, sentence):
        self.sentence = sentence



    def add_rhyme(self, nrhyme):
        self.rhyme = nrhyme