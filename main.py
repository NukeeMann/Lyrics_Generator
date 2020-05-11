from Word import Word
import re
import random
import os
from os import listdir
from os.path import isfile, join

def load_file(file_name, phon_name, dict, rhyme_dict):
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

    for bsword, bword, word, first, second, third, rhyme_word in zip(words[0:],words[1:], words[2:], words[3:], words[4:], words[5:], phonetics[2:]) :

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
        dict[word].add_second_bword(bsword)

    return


def generate_word(dicti, rhyme_words, base_word, prev_word, prev_prev_word, prev_rhyme):
    # Jezeli slowa nie ma w slowniku losuj jakiekolwiek
    if base_word not in dicti.keys():
        return random.choice(list(dicti.keys()))

    # Jezeli po slowie nie wystepuje nigdy inne slowo losuj dowolne
    if len(dicti[base_word].get_first_word_dic()) < 0:
        return random.choice(list(dicti.keys()))

    chance = random.random()
    stack_prob = 0.0
    FOUR_COMMON = 4.0
    THREE_COMMON = 4.0

    # Jezeli jest polaczenie miedzy dwoma poprzednimi wyrazami, obecnym i nastepnym
    for bsword_third in dicti[prev_prev_word].get_third_word_dic():
        for bword_second in dicti[prev_word].get_second_word_dic():
            for word_first in dicti[base_word].get_first_word_dic():
                if bword_second[0] == word_first[0] and word_first[0] == bsword_third[0] and word_first[0] != base_word:
                    if word_first[0] in rhyme_words:
                        return word_first[0]
                    else:
                        prob4 = stack_prob + FOUR_COMMON*(word_first[1] + bword_second[1] + bsword_third[1])
                        if prob4 > chance:
                            return word_first[0]

    # Jezeli jest polaczenie miedzy poprzednim wyraze, obecnym i nastepnym
    for bword_second in dicti[prev_word].get_second_word_dic():
        for word_first in dicti[base_word].get_first_word_dic():
            if bword_second[0] == word_first[0] and word_first[0] != base_word:
                if word_first[0] in rhyme_words:
                    return word_first[0]
                else:
                    prob3 = stack_prob + THREE_COMMON*(word_first[1] + bword_second[1])
                    if prob3 > chance:
                        return word_first[0]

    # Jezeli jest poleczenie miedzy obecnym i nastepnym wyrazem i jest rym
    for nword in dicti[base_word].get_first_word_dic():
        if nword[0] in rhyme_words:
            return nword[0]

    return random.choice(list(dicti[base_word].get_first_word_dic()))[0]


def generate_lyrcis(dict, rhyme_dict, word):
    lyrcis = []
    lyrcis.append(word)
    word = generate_word(dict, '', word, word, word, 'null')
    lyrcis.append(word)
    prev_word = word
    prev_prev_word = word


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
                word = generate_word(dict, rhyme_dict[rhyme], word, prev_word, prev_prev_word,rhymes[0])
                prev_prev_word = prev_word
                prev_word = prev_word_tmp
                # Poczatek zdania
                if words_in_line == 0:
                    lyrcis.append(word.capitalize())
                else:
                    lyrcis.append(word)
                words_in_line = words_in_line + 1

                # Jezeli zdanie jest za dlugie
                if words_in_line > 10:
                    if len(list(rhyme_dict[rhyme])) > 1 and rhymes[0] != 'null':
                        iterator  = 0

                        # Szukanie slowa rymujacego sie
                        for fake_rhyme in rhyme_dict[rhyme]:
                            if fake_rhyme != rhymes[0] and word != fake_rhyme:
                                for tuple_word in dict[word].get_first_word_dic():
                                    if fake_rhyme == tuple_word[0]:
                                        word = fake_rhyme
                                        break
                            iterator = iterator + 1

                        if iterator >= len(rhyme_dict[rhyme]):
                            while True:
                                word = random.choice(list(rhyme_dict[rhyme]))
                                if word != rhymes[0]:
                                    break
                    else:
                        word = random.choice(list(rhyme_dict[rhyme]))
                    lyrcis.append(word)

                # Jezeli wyraz wylosowany jest w slowniku rymow, przechodzi do kolejnego zdania
                if word in rhyme_dict[rhyme] and words_in_line > 4:
                    rhymes[rhyme_index] = word
                    rhyme_index = rhyme_index + 1
                    lyrcis.append('\n')
                    break
        lyrcis.append('\n')




    lyrcis = " ".join(lyrcis)
    return lyrcis


if __name__ == '__main__':
    # Przechowuje slowa
    dictionary = {}

    # Przechowuje rymy i slowa do tych rymow
    rhyme_dictionary = {}

    for f in listdir('database/'):
        if '.txt' in f:
            file_Name = 'database/' + f
            phon_Name = 'database/phonetics/PHON_' + f
            load_file(file_Name, phon_Name, dictionary, rhyme_dictionary)



    for word in dictionary:
        dictionary[word].count_probability()
        dictionary[word].sort()


    print(generate_lyrcis(dictionary, rhyme_dictionary, ""))
