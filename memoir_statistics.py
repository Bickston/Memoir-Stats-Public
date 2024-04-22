from statistics import mean, stdev, median_high, mode
from datetime import datetime
from utils import get_posts, clean_text, track_days, get_sentences

# Update this whenever you cross the International Date Line in the Eastward direction and post on both sides
ALLOWED_ERROR_HOURS = 1


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
    standardized_dates = []
    date_differences = []

    matched_dates = track_days(pdf_text)

    for date_str in matched_dates:
        standardized_dates.append(datetime.strptime(date_str, "%m/%d/%y"))

    previous_date = standardized_dates[0]

    for standardized_date in standardized_dates[1:]:
        days_difference = (standardized_date - previous_date).days

        if days_difference < 0:
            raise ValueError("Some dates are out of order in the memoir near {}/{}/{}".format(standardized_date.month,
                                                                                              standardized_date.day,
                                                                                              standardized_date.year))
        date_differences.append(days_difference)
        previous_date = standardized_date

    print_statistics(date_differences, "days", "between", "posts")


def find_hours_data(pdf_text):
    standardized_dates = []
    hour_differences = []
    error_hours = 0

    matched_dates = track_days(pdf_text, True)

    for date_str in matched_dates:
        standardized_dates.append(datetime.strptime(date_str, "%m/%d/%y %I:%M%p"))

    previous_date = standardized_dates[0]

    for standardized_date in standardized_dates[1:]:
        hours_difference = round((standardized_date - previous_date).total_seconds() / 3600, 2)

        if hours_difference < 0:
            error_hours += 1

        hour_differences.append(hours_difference)
        previous_date = standardized_date

    if error_hours > ALLOWED_ERROR_HOURS:
        raise ValueError("Some hours are out of order in the memoir")

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
    print(f"Total words: {len(clean_text(pdf_text).split())}")
    print(f"Total characters: {len(pdf_text)}")
    print()
