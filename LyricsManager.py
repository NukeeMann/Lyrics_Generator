from Word import Word
import re
import random
import os
from os import listdir
from os.path import isfile, join
from Display import *

class LyricsManager:

    def __init__(self):
        # Przechowuje slowa
        self.dictionary = {}

        # Przechowuje rymy i slowa do tych rymow
        self.rhyme_dictionary = {}

        self.mainWindow = Window(600, 400, self)

    def createByArtist(self, artist):
        for f in listdir('database/' + artist +'/'):
            if '.txt' in f:
                file_Name = 'database/' + artist +'/' + f
                phon_Name = 'database/' + artist  +'/' + 'phonetics/PHON_' + f
                self.load_file(file_Name, phon_Name, self.dictionary, self.rhyme_dictionary)

        for word in self.dictionary:
            self.dictionary[word].count_probability()

        self.windowText = WindowText(self.generate_lyrcis(self.dictionary, self.rhyme_dictionary, random.choice(list(self.dictionary.keys()))))
        self.dictionary = {}
        self.rhyme_dictionary = {}

    def createFromAllTexts(self):
        for dire in listdir('database/'):
            for f in listdir('database/'+dire+'/'):
                if '.txt' in f:
                    file_Name = 'database/' + dire + '/' + f
                    phon_Name = 'database/'+dire+'/phonetics/PHON_' + f
                    self.load_file(file_Name, phon_Name, self.dictionary, self.rhyme_dictionary)

        for word in self.dictionary:
            self.dictionary[word].count_probability()

        self.windowText = WindowText(self.generate_lyrcis(self.dictionary, self.rhyme_dictionary, random.choice(list(self.dictionary.keys()))))
        self.dictionary = {}
        self.rhyme_dictionary = {}

    def createBySong(self, list):
        for song in list:
            file_Name = 'database/Yours/' + song
            phon_Name = 'database/Yours/phonetics/PHON_' + song
            self.load_file(file_Name, phon_Name, self.dictionary, self.rhyme_dictionary)

        for word in self.dictionary:
            self.dictionary[word].count_probability()

        self.windowText = WindowText(self.generate_lyrcis(self.dictionary, self.rhyme_dictionary, random.choice(list(self.dictionary.keys()))))
        self.dictionary = {}
        self.rhyme_dictionary = {}

    #Laduje plik wraz z wymowa do dwoch slownikow tworzy polaczenia miedzy wyrazamia
    def load_file(self,file_name, phon_name, dict, rhyme_dict):
        file = open(file_name, encoding="utf8")
        words = re.sub("\n", " ", file.read().lower())
        words = words.replace(',', '')
        words = words.replace('.', '')
        words = words.replace('!', '')
        words = words.replace('(', '')
        words = words.replace(')', '')
        words = words.replace('"', '')
        words = words.replace('?', '').split(' ')

        phon_file = open(phon_name, encoding="utf8")
        phonetics = re.sub("\n", " ", phon_file.read())
        phonetics = phonetics.replace(',', '')
        phonetics = phonetics.replace('.', '')
        phonetics = phonetics.replace('!', '')
        phonetics = phonetics.replace('(', '')
        phonetics = phonetics.replace(')', '')
        phonetics = phonetics.replace('"', '')
        phonetics = phonetics.replace('?', '').split(' ')

        for bsword, bword, word, first, second, third, rhyme_word in zip(words[0:], words[1:], words[2:], words[3:],
                                                                         words[4:], words[5:], phonetics[2:]):

            # Ucinamy rym do ostatnich 2 dzwiekow
            if len(rhyme_word) > 3:
                rhyme_word = rhyme_word[len(rhyme_word) - 3] + rhyme_word[len(rhyme_word) - 2] + rhyme_word[
                    len(rhyme_word) - 1]

            if len(rhyme_word) > 2:
                if rhyme_word not in rhyme_dict.keys():
                    rhyme_dict[rhyme_word] = [word]
                else:
                    if word not in rhyme_dict[rhyme_word]:
                        rhyme_dict[rhyme_word] = rhyme_dict[rhyme_word] + [word]

            if word not in dict:
                dict[word] = Word(word)

            dict[word].add_rhyme(rhyme_word)
            dict[word].add_first_nword(first)
            dict[word].add_second_nword(second)
            dict[word].add_third_nword(third)
            dict[word].add_first_bword(bword)
            dict[word].add_second_bword(bsword)

        return

    def generate_word(self, dicti, rhyme_words, base_word, prev_word, prev_prev_word, prev_rhyme):
        # Jezeli slowa nie ma w slowniku losuj jakiekolwiek
        if base_word not in dicti.keys():
            return random.choice(list(dicti.keys()))

        # Jezeli po slowie nie wystepuje nigdy inne slowo losuj dowolne
        if len(dicti[base_word].get_first_word_dic()) < 0:
            return random.choice(list(dicti.keys()))

        nword_probability = {}
        iterator = 0
        first_nword = dicti[base_word].get_first_word_dic()
        for nword in first_nword.keys():
            if nword != prev_word and nword != prev_prev_word and nword != base_word:
                nword_probability[nword] = first_nword[nword]
                second_nword = dicti[prev_word].get_second_word_dic()
                if nword in second_nword.keys():
                    nword_probability[nword] = nword_probability[nword] + second_nword[nword]
                    third_word = dicti[prev_prev_word].get_third_word_dic()
                    if nword in third_word.keys():
                        nword_probability[nword] = nword_probability[nword] + third_word[nword]

        best_word_1 = ' '
        prob = 0
        for nword in nword_probability.keys():
            if best_word_1 == ' ':
                best_word_1 = nword
                prob = nword_probability[nword]
            else:
                if best_word_1 in rhyme_words:
                    prob *= 1.2
                if nword_probability[nword] > prob:
                    best_word_1 = nword
                    prob = nword_probability[nword]

        best_word_2 = ' '
        prob = 0
        for nword in nword_probability.keys():
            if nword != best_word_1:
                if best_word_2 == ' ':
                    best_word_2 = nword
                    prob = nword_probability[nword]
                else:
                    if best_word_2 in rhyme_words:
                        prob *= 1.2
                    if nword_probability[nword] > prob:
                        best_word_2 = nword
                        prob = nword_probability[nword]

        if best_word_1 == ' ':
            return random.choice(list(dicti[base_word].get_first_word_dic().keys()))

        if best_word_2 == ' ':
            return best_word_1

        if random.random() > 0.4:
            return best_word_1
        else:
            return best_word_2

    def force_rhyme(self, dict, rhyme_dict, rhyme, rhymes, word):
        if len(list(rhyme_dict[rhyme])) > 1 and rhymes[0] != 'null':
            iterator = 0

            # Szukanie slowa rymujacego sie
            for fake_rhyme in rhyme_dict[rhyme]:
                if fake_rhyme != rhymes[0] and word != fake_rhyme and word != ' ' and word != '':
                    if fake_rhyme in dict[word].get_first_word_dic().keys():
                        return fake_rhyme

                iterator = iterator + 1

            if iterator >= len(rhyme_dict[rhyme]):
                while True:
                    word = random.choice(list(rhyme_dict[rhyme]))
                    if word != rhymes[0]:
                        return word
        else:
            word = random.choice(list(rhyme_dict[rhyme]))
            if rhyme[0] != word:
                return word
            else:
                return random.choice(list(rhyme_dict[rhyme]))

    def generate_lyrcis(self, dict, rhyme_dict, word):
        lyrcis = []
        lyrcis.append(word.capitalize())
        prev_word = word
        prev_prev_word = word
        word = self.generate_word(dict, [], word, prev_word, prev_prev_word, 'null')
        lyrcis.append(word)

        for i in range(20):
            # LOSUJE RYM
            while True:
                rhyme = random.choice(list(rhyme_dict.keys()))
                if len(rhyme_dict[rhyme]) > 3:
                    break
            rhymes = ['null', 'null']
            for i in range(2):
                rhyme_index = 0
                words_in_line = 0

                while True:
                    prev_word_tmp = word  # Poprzedni wyraz ktory wystapil
                    word = self.generate_word(dict, rhyme_dict[rhyme], word, prev_word, prev_prev_word, rhymes[0])
                    prev_prev_word = prev_word
                    prev_word = prev_word_tmp
                    words_in_line = words_in_line + 1

                    # Poczatek zdania
                    if words_in_line == 1:
                        lyrcis.append(word.capitalize())
                    else:
                        lyrcis.append(word)

                    # Jezeli zdanie jest za dlugie wymus dodanie rymu
                    if words_in_line > 8:
                        if rhymes[0] == 'null':
                            for key, values in rhyme_dict.items():
                                if word in values:
                                    rhymes[0] = word
                                    rhyme = key
                        else:
                            prev_word_tmp = word
                            word = self.force_rhyme(dict, rhyme_dict, rhyme, rhymes, word)
                            prev_prev_word = prev_word
                            prev_word = prev_word_tmp
                            lyrcis.append(word)

                    # Jezeli wyraz wylosowany jest w slowniku rymow, przechodzi do kolejnego zdania
                    if word in rhyme_dict[rhyme] and words_in_line > 3:
                        rhymes[rhyme_index] = word
                        rhyme_index = rhyme_index + 1
                        lyrcis.append('\n')
                        break
            lyrcis.append('\n')

        lyrcis = " ".join(lyrcis)
        return lyrcis
