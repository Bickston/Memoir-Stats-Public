import create_text_file
import memoir_counts
import memoir_statistics
import graphing


# DEFINITIONS
# XXX Count - the total number of times that item appears in the memoir
# XXX Frequency - the total number of posts that item appears in


# PATHS

memoir_path = '/Users/BickstonL/Documents/Personal/Personal Documents/Memoir/Memoir VOLUME 2.0.pdf'
txt_path = './memoir.txt'
dictionary_path = './dictionary.txt'


# PRE-PROCESSING

# Takes the current memoir and turns it into a .txt file (ONLY RUN THIS ONCE)
# create_text_file.extract_text_from_pdf(memoir_path, txt_path)

# Takes the text file and turns it into a single string
pdf_text = create_text_file.get_extracted_text(txt_path)


# CHARACTER AND WORD COUNTS

# Counts and prints out characters in order of use. Default is any character used more than once.
# Params: pdf_text, min_occurrences=2, alpha_only=False, include_punc=False
memoir_counts.count_characters(pdf_text)

# Counts and prints out words in order of use. Default is any word used at least 40 times.
# Params: pdf_text, dictionary_path, min_occurrences=40, in_dic=True
# memoir_counts.count_words(pdf_text, dictionary_path)

# Counts and prints out first words in each post in order of use. Default is all words.
# Params: pdf_text, min_occurrences=1
# memoir_counts.count_first_words(pdf_text)

# Counts the number of times a word appears anywhere in a post. Default is words in at least 120 posts.
# Params: pdf_text, min_occurrences=120
# memoir_counts.count_word_frequency(pdf_text)

# Counts the frequency of most used phrases of passed in length. Default is 2-word phrases that appear >= 200 times.
# Params: pdf_text, words_in_phrase=2, min_occurrences=200
# memoir_counts.count_phrases(pdf_text)

# Gives the ratio of word frequency to word count. Default is words used >= 100 times.
# Params: pdf_text, min_occurrences=100
# memoir_counts.find_consistent_words(pdf_text)


# MEMOIR STATISTICS

# Returns the total post count, total word count, and total character count
# memoir_statistics.find_totals(pdf_text)

# Returns the mean, standard deviation, median, mode, maximum, and minimum word length
# memoir_statistics.find_word_length_data(pdf_text)

# Returns the mean, standard deviation, median, mode, maximum, and minimum sentence length
# memoir_statistics.find_sentence_length_data(pdf_text)

# Returns the mean, standard deviation, median, mode, maximum, and minimum post length
# memoir_statistics.find_post_length_data(pdf_text)

# Returns the mean, standard deviation, median, mode, maximum, and minimum days between posting
# memoir_statistics.find_days_data(pdf_text)

# Returns the mean, standard deviation, median, mode, maximum, and minimum hours between posting
# memoir_statistics.find_hours_data(pdf_text)


# GRAPHING

# Graphs words per post including everything with a line of best fit
# graphing.graph_words_scatterplot(pdf_text)

# Graphs what time of day I post in histogram form by hour
# graphing.make_hour_histogram(pdf_text)

# Graphs what time of day I post in circular histogram form by hour
# graphing.make_hour_circular_histogram(pdf_text)

# Graphs what time of day I post in histogram form by half hour
# graphing.make_half_hour_histogram(pdf_text)

# Graphs what time of day I post in histogram form by quarter-hour
# graphing.make_quarter_hour_histogram(pdf_text)

# Graphs what day of the week I post
# graphing.graph_day_of_week(pdf_text)

# Graphs what day of the month I post
# graphing.graph_day_of_month(pdf_text)

# Graphs word length frequency. Default only includes words shorter than 12 letters and labels.
# Params: pdf_text, include_labels=True, max_length=12
# graphing.graph_word_length_frequency(pdf_text)

# Graphs sentence length frequency. Default only includes sentences shorter than 70 words and no labels.
# Params: pdf_text, include_labels=False, max_length=70
# graphing.graph_sentence_length_frequency(pdf_text)

# Graphs post length frequency in a histogram. Default includes posts with less than 10000 words.
# Params: pdf_text, max_length=10000
# graphing.graph_post_length_frequency(pdf_text) # TODO: improve

# Graphs the word frequency per post in a scatterplot
# graphing.graph_certain_word_frequency(pdf_text, "the") # TODO: normalize against post word count
