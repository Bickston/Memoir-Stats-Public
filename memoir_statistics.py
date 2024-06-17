from statistics import mean, stdev, median_high, mode
from datetime import datetime
from utils import get_posts, clean_text, get_sentences, days_helper, hours_helper, track_days


def print_statistics(stat_list, thing, perbtw="per", item="post"):
    avg = round(mean(stat_list), 2)
    std = round(stdev(stat_list), 2)
    med = round(median_high(stat_list), 2)
    mod = round(mode(stat_list), 2)
    maxi = round(max(stat_list), 2)
    mini = round(min(stat_list), 2)

    print(f"Average {thing} {perbtw} {item}: {avg}")
    print(f"Standard deviation in {thing} {perbtw} {item}: {std}")
    print(f"Median {thing} {perbtw} {item}: {med}")
    if len(stat_list) == len(set(stat_list)):
        print("No mode.")
    else:
        print(f"Mode {thing} {perbtw} {item}: {mod}")
    print(f"Maximum {thing} {perbtw} {item}: {maxi}")
    print(f"Minimum {thing} {perbtw} {item}: {mini}")
    print()


def standardize_date(date_str):
    parts = date_str.split('/')

    month = parts[0].zfill(2)
    day = parts[1].zfill(2)

    year_format = "%y" if len(parts[2]) == 2 else "%Y"
    year = datetime.strptime(parts[2], year_format).strftime("%Y")
    standardized_date = f"{month}/{day}/{year}"

    return standardized_date


def find_days_data(pdf_text):
    date_differences = days_helper(pdf_text)

    print_statistics(date_differences, "days", "between", "posts")


def find_hours_data(pdf_text):
    hour_differences = hours_helper(pdf_text)

    print_statistics(hour_differences, "hours", "between", "posts")


def find_post_length_data(pdf_text):
    posts = get_posts(pdf_text)

    word_counts = [len(post.split()) for post in posts[1:]]

    print_statistics(word_counts, "words")


def find_sentence_length_data(pdf_text):
    sentences = get_sentences(pdf_text)

    word_counts = [len(sentence.split()) for sentence in sentences[1:]]

    print_statistics(word_counts, "words", item="sentence")


def find_word_length_data(pdf_text):
    cleaned_text = clean_text(pdf_text)

    words = cleaned_text.split()

    word_lengths = [len(word) for word in words]

    print_statistics(word_lengths, "characters", item="word")


def find_totals(pdf_text):
    print(f"Total posts: {len(get_posts(pdf_text))}")
    print(f"Total sentences: {len(get_sentences(pdf_text))}")
    print(f"Total words: {len(clean_text(pdf_text).split())}")
    print(f"Total characters: {len(pdf_text)}")
    print()


def find_time_since_start(pdf_text):
    dates = track_days(pdf_text)

    days_difference = datetime.today().date() - datetime.strptime(dates[0], "%m/%d/%y").date()

    print(f"Days since first post: {days_difference.days}")
    print(f"Years since first post: {(days_difference.days / 365):.2f}")
    print(f"Average words per day: {len(clean_text(pdf_text).split()) // days_difference.days}")
    print(f"Average words per year: {len(clean_text(pdf_text).split()) // days_difference.days * 365}")
    print()
