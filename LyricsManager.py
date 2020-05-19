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

        self.windowText = WindowText(self.generate_lyrcis(self.dictionary, self.rhyme_dictionary, ""))
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

        self.windowText = WindowText(self.generate_lyrcis(self.dictionary, self.rhyme_dictionary, ""))
        self.dictionary = {}
        self.rhyme_dictionary = {}

    def createBySong(self, list):
        for song in list:
            file_Name = 'database/Yours/' + song
            phon_Name = 'database/Yours/phonetics/PHON_' + song
            self.load_file(file_Name, phon_Name, self.dictionary, self.rhyme_dictionary)

        for word in self.dictionary:
            self.dictionary[word].count_probability()

        self.windowText = WindowText(self.generate_lyrcis(self.dictionary, self.rhyme_dictionary, ""))
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
        words = words.replace('?', '').split(' ')

        phon_file = open(phon_name, encoding="utf8")
        phonetics = re.sub("\n", " ", phon_file.read())
        phonetics = phonetics.replace(',', '')
        phonetics = phonetics.replace('.', '')
        phonetics = phonetics.replace('!', '')
        phonetics = phonetics.replace('(', '')
        phonetics = phonetics.replace(')', '')
        phonetics = phonetics.replace('?', '').split(' ')

        for bword, word, first, second, third, rhyme_word in zip(words[0:],words[1:], words[2:], words[3:], words[4:], phonetics[1:]) :

            # Ucinamy rym do ostatnich 2 dzwiekow
            if len(rhyme_word) > 3:
                rhyme_word = rhyme_word[len(rhyme_word) - 3] + rhyme_word[len(rhyme_word) - 2] + rhyme_word[len(rhyme_word) - 1]

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

        return


    def generate_word(self, dict, base_word, rhyme_words, prev_word, prev_rhyme):
        # Jezeli slowa nie ma w slowniku losuj jakiekolwiek
        if base_word not in dict.keys():
            return random.choice(list(dict.keys()))

        # Jezeli po slowie nie wystepuje nigdy inne slowo losuj dowolne
        if len(dict[base_word].get_first_word_dic()) < 0:
            return random.choice(list(dict.keys()))

        # SPRAWDZENIE CZY PIERWSZY NASTEPNY WYRAZ SIE RYMUJE
        first_nwords = dict[base_word].get_first_word_dic()
        for n1word in first_nwords.keys():
            if n1word in rhyme_words and n1word != prev_rhyme:
                return n1word

        # SPRAWDZENIE CZY DRUGI NASTEPNY WYRAZ SIE RYMUJE
        second_nwords = dict[base_word].get_second_word_dic()
        for n2word in second_nwords.keys():
            # Jezeli rym jest w drugim nastepnym wyrazie
            if n2word in rhyme_words and n2word != prev_rhyme:
                second_bwords = dict[n2word].get_before_word_dic()
                word_first = dict[base_word].get_first_word_dic()
                for next_word in second_bwords:
                    # Szukanie nastepnego wyrazu
                    if next_word in word_first:
                        return next_word

        # SPRAWDZENIE CZY TRZECI NASTEPNY WYRAZ SIE RYMUJE
        third_words = dict[base_word].get_third_word_dic()
        for n3word in third_words.keys():
            # Jezeli rym jest w trzecim nastepnym wyrazie
            if n3word in rhyme_words and n3word != prev_rhyme:
                third_bwords = dict[n3word].get_before_word_dic()
                word_second = dict[base_word].get_second_word_dic()
                for n3bword in third_bwords.keys():
                    # Jezeli drugi nword jest taki sam jak bword trzeciego nword "lacznik miedzy wyrazami"
                    if n3bword in word_second:
                        third_bword_bwords = dict[n3bword].get_before_word_dic()
                        word_first = dict[base_word].get_first_word_dic()
                        for next_word in third_bword_bwords:
                            # Szukanie nastepnego wyrazu
                            if next_word in word_first:
                                return next_word





        chance = random.random()
        stack_prob = 0.0
        first_nword = dict[base_word].get_first_word_dic()
        for nword in first_nword.keys():

            if nword in rhyme_words:
                stack_prob = stack_prob + 1.5*first_nword[nword]
            else:
                stack_prob = stack_prob + first_nword[nword]

            bword = dict[prev_word].get_second_word_dic()
            if nword in bword.keys():
                stack_prob = stack_prob + bword[nword]

            # if X wyraz

            if stack_prob > chance:
                return nword

            if nword in rhyme_words:
                stack_prob = stack_prob - 1.5*first_nword[nword]
                stack_prob = stack_prob + first_nword[nword]

            if nword in bword.keys():
                stack_prob = stack_prob - bword[nword]

        return base_word


    def generate_lyrcis(self, dict, rhyme_dict, word):
        lyrcis = []
        lyrcis.append(word)
        word = self.generate_word(dict, word, '', word, 'null')
        lyrcis.append(word)
        prev_word = word


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
                    prev_word_tmp = word    # Poprzedni wyraz ktory wystapil
                    word = self.generate_word(dict, word, rhyme_dict[rhyme], prev_word, rhymes[0])
                    prev_word = prev_word_tmp
                    lyrcis.append(word)
                    words_in_line = words_in_line + 1
                    if words_in_line > 10:
                        if len(list(rhyme_dict[rhyme])) > 1 and rhymes[0] != 'null':
                            while True:
                                word = random.choice(list(rhyme_dict[rhyme]))
                                if word != rhymes[0]:
                                    break
                        else:
                            word = random.choice(list(rhyme_dict[rhyme]))
                        lyrcis.append(word)
                    if word in rhyme_dict[rhyme] and words_in_line > 4:
                        rhymes[rhyme_index] = word
                        rhyme_index = rhyme_index + 1
                        lyrcis.append('\n')
                        break
            lyrcis.append('\n')




        lyrcis = " ".join(lyrcis)
        return lyrcis
