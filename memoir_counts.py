from utils import get_posts, clean_text


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


def count_characters(pdf_text, min_occurrences=2, alpha_only=False):
    char_dic = {}

    pdf_text = pdf_text.lower()

    for character in pdf_text:
        if character not in char_dic and (not alpha_only or character.isalpha()):
            char_dic[character] = 0
        if character in char_dic:
            char_dic[character] += 1

    print_chars_and_words(char_dic, 14, min_occurrences)


def count_words(pdf_text, dic_path, min_occurrences=40, no_dic=True):
    # TODO: change to a counter
    cleaned_text = clean_text(pdf_text)
    dictionary = make_dictionary(dic_path)

    word_count = {}
    for word in cleaned_text.split():
        if word not in word_count and (not no_dic or word not in dictionary):
            word_count[word] = 0
        if word in word_count:
            word_count[word] += 1

    print_chars_and_words(word_count, 18, min_occurrences)


def count_first_words(pdf_text, min_occurrences=1):
    posts = get_posts(pdf_text)
    word_count = {}

    for post in posts:
        word = post.split()[0].strip(" ,()")
        if word not in word_count:
            word_count[word] = 0
        word_count[word] += 1

    print_chars_and_words(word_count, 18, min_occurrences)


def count_word_frequency(pdf_text, min_occurrences=120):
    posts = get_posts(pdf_text)
    word_dictionary = {}

    for post in posts:
        word_set = set()

        for word in post.split():
            word = word.strip('''."'”“()[]?!,:;''')
            word_set.add(word)

        for word in word_set:
            if word not in word_dictionary:
                word_dictionary[word] = 0
            word_dictionary[word] += 1

    print_chars_and_words(word_dictionary, 22, min_occurrences)
