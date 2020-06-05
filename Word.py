import operator

class Word:
    def __init__(self, word):
        self.word = word
        self.first_bword = {}
        self.first_nword = {}
        self.second_nword = {}
        self.third_nword = {}
        self.rhyme = 'null'

    # Funkcje
    def count_probability(self):
        count = 0
        # Zliczanie
        for word in self.first_nword.keys():
            count += int(self.first_nword.get(word))

        # Obliczanie prawdopodobienstwa
        for word in self.first_nword.keys():
            self.first_nword[word] = self.first_nword.get(word) / float(count)

        count = 0
        # Zliczanie
        for word in self.second_nword.keys():
            count += int(self.second_nword.get(word))

        # Obliczanie prawdopodobienstwa
        for word in self.second_nword.keys():
            self.second_nword[word] = self.second_nword.get(word) / float(count)

        count = 0
        # Zliczanie
        for word in self.third_nword.keys():
            count += int(self.third_nword.get(word))

        # Obliczanie prawdopodobienstwa
        for word in self.third_nword.keys():
            self.third_nword[word] = self.third_nword.get(word) / float(count)

        count = 0
        # Zliczanie
        for word in self.first_bword.keys():
            count += int(self.first_bword.get(word))

        # Obliczanie prawdopodobienstwa
        for word in self.first_bword.keys():
            self.first_bword[word] = self.first_bword.get(word) / float(count)



    # Getery
    def get_first_word_dic(self):
        return self.first_nword

    def get_second_word_dic(self):
        return self.second_nword

    def get_third_word_dic(self):
        return self.third_nword

    def get_before_word_dic(self):
        return self.first_bword

    def get_rhyme(self):
        return self.rhyme

    # Setery
    def add_first_nword(self, nword):
        if nword not in self.first_nword.keys():
            self.first_nword[nword] = 1
        else:
            self.first_nword[nword] = self.first_nword[nword] + 1

    def add_second_nword(self, nword):
        if nword not in self.second_nword.keys():
            self.second_nword[nword] = 1
        else:
            self.second_nword[nword] = self.second_nword[nword] + 1

    def add_third_nword(self, nword):
        if nword not in self.third_nword.keys():
            self.third_nword[nword] = 1
        else:
            self.third_nword[nword] = self.third_nword[nword] + 1

    def add_first_bword(self, bword):
        if bword not in self.first_bword.keys():
            self.first_bword[bword] = 1
        else:
            self.first_bword[bword] = self.first_bword[bword] + 1

    def add_rhyme(self, nrhyme):
        self.rhyme = nrhyme