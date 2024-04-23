from utils import get_posts, clean_text
from collections import Counter


def make_dictionary(dictionary_path):
    with open(dictionary_path) as file:
        return set([line.strip() for line in file])


def print_chars_and_words(dictionary, line_length, min_occurrences):
    sorted_dictionary = sorted(dictionary.items(), key=lambda x: -x[1])

    line_dictionary = {}
    for i in range(10):
        line_dictionary[i] = ""

    for num, (key, value) in enumerate(sorted_dictionary):
        if value <= min_occurrences - 1:
            break
        if key != '\n':
            entry = str(num + 1) + ". " + key + ": " + str(value)
            while len(entry) < line_length:
                entry += ' '
            line_dictionary[num % 10] += entry
        else:
            entry = str(num + 1) + ". \\: " + str(value)
            while len(entry) < line_length:
                entry += ' '
            line_dictionary[num % 10] += entry

    for string in line_dictionary:
        print(line_dictionary[string])


def get_char_count_dic(pdf_text):
    return Counter(clean_text(pdf_text))


def count_characters(pdf_text, min_occurrences=2, alpha_only=False, include_punc=False):
    if include_punc:
        char_dic = {}
        pdf_text = pdf_text.lower()
        for character in pdf_text:
            if character not in char_dic and (not alpha_only or character.isalpha()):
                char_dic[character] = 0
            if character in char_dic:
                char_dic[character] += 1
    else:
        char_dic = get_char_count_dic(pdf_text)
        for key in list(char_dic.keys()):
            if alpha_only and not key.isalpha():
                del char_dic[key]

    print_chars_and_words(char_dic, 14, min_occurrences)


def get_word_count_dic(pdf_text):
    return Counter(clean_text(pdf_text).split())


def count_words(pdf_text, dic_path, min_occurrences=40, in_dic=True):
    counter = get_word_count_dic(pdf_text)

    if not in_dic:
        dictionary = make_dictionary(dic_path)
        for key in list(counter.keys()):
            if key in dictionary:
                del counter[key]

    print_chars_and_words(counter, 18, min_occurrences)


def count_first_words(pdf_text, min_occurrences=1):
    posts = get_posts(pdf_text)
    word_count = {}

    for post in posts:
        word = post.split()[0].strip(" ,()")
        if word not in word_count:
            word_count[word] = 0
        word_count[word] += 1

    print_chars_and_words(word_count, 18, min_occurrences)


def get_word_freq_dic(pdf_text):
    posts = get_posts(pdf_text)
    word_dictionary = {}

    for post in posts:
        word_set = set()

        for word in post.split():
            word = clean_text(word)
            word_set.add(word)

        for word in word_set:
            if word not in word_dictionary:
                word_dictionary[word] = 0
            word_dictionary[word] += 1

    return word_dictionary


def count_word_frequency(pdf_text, min_occurrences=120):
    print_chars_and_words(get_word_freq_dic(pdf_text), 22, min_occurrences)


def count_phrases(pdf_text, words_in_phrase=2, min_occurrences=200):
    text = clean_text(pdf_text).split()
    phrase_dic = {}

    for i in range(len(text) - words_in_phrase + 1):
        phrase = ""
        for j in range(i, i + words_in_phrase):
            phrase += text[j] + " "
        phrase = phrase.strip()

        if phrase not in phrase_dic:
            phrase_dic[phrase] = 0
        phrase_dic[phrase] += 1

    print_chars_and_words(phrase_dic, 10 * words_in_phrase, min_occurrences)


def find_consistent_words(pdf_text, min_occurrences=100):
    word_freq_dictionary = get_word_freq_dic(pdf_text)
    word_count_dictionary = get_word_count_dic(pdf_text)

    consistency_dic = {}

    for key, value in word_freq_dictionary.items():
        count = word_count_dictionary[key]
        if len(key) != 0 and count >= min_occurrences:
            consistency_dic[key] = round(value ** 2 / count, 2)

    print_chars_and_words(consistency_dic, 22, 0)
