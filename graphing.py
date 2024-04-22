from scipy.stats import linregress
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from utils import track_days, get_posts, clean_text, get_sentences
from collections import Counter
import re


def make_hour_histogram(pdf_text):
    days_and_hours = track_days(pdf_text, True)
    hours = [datetime.strptime(dt_str, '%m/%d/%y %I:%M%p').hour for dt_str in days_and_hours]
    hour_counts = [hours.count(hour) for hour in range(24)]

    plt.figure(figsize=(10, 5))
    plt.bar(range(24), hour_counts, color='skyblue')
    plt.xlabel('Hour of the day')
    plt.ylabel('Frequency')
    plt.title('24-Hour Histogram')
    plt.xticks(range(24))
    plt.grid(True)
    plt.show()


def make_hour_circular_histogram(pdf_text):
    days_and_hours = track_days(pdf_text, True)
    hours = [datetime.strptime(dt_str, '%m/%d/%y %I:%M%p').hour for dt_str in days_and_hours]
    hour_counts = [hours.count(hour) for hour in range(24)]

    angles = np.linspace(0, 2 * np.pi, len(hour_counts), endpoint=False).tolist()
    hour_counts.append(hour_counts[0])
    angles.append(angles[0])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    ax.plot(angles, hour_counts, marker='o', color='skyblue')
    ax.fill(angles, hour_counts, color='skyblue', alpha=0.25)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
    ax.set_xticklabels([str(i) for i in range(24)])
    ax.set_title('Circular Histogram of Hourly Events')
    plt.show()


def make_half_hour_histogram(pdf_text):
    days_and_hours = track_days(pdf_text, True)
    hours_minutes = [
        datetime.strptime(dt_str, '%m/%d/%y %I:%M%p').hour + datetime.strptime(dt_str, '%m/%d/%y %I:%M%p').minute / 60
        for dt_str in days_and_hours]

    half_hours = [math.floor(x * 2) / 2 for x in hours_minutes]

    half_hour_counts = [half_hours.count(i) for i in np.arange(0.0, 24.0, 0.5)]

    plt.figure(figsize=(12, 6))
    plt.bar(np.arange(0, 24, 0.5), half_hour_counts, color='skyblue', width=0.4, align='center')
    plt.xlabel('Half-hour of the day')
    plt.ylabel('Frequency')
    plt.title('Half-hourly Histogram')
    plt.xticks(range(24))
    plt.grid(True)
    plt.show()


def make_quarter_hour_histogram(pdf_text):
    days_and_hours = track_days(pdf_text, True)
    hours_minutes = [
        datetime.strptime(dt_str, '%m/%d/%y %I:%M%p').hour + datetime.strptime(dt_str, '%m/%d/%y %I:%M%p').minute / 60
        for dt_str in days_and_hours]

    quarter_hours = [math.floor(x * 4) / 4 for x in hours_minutes]

    quarter_hour_counts = [quarter_hours.count(i) for i in np.arange(0.0, 24.0, 0.25)]

    plt.figure(figsize=(14, 7))
    plt.bar(np.arange(0, 24, 0.25), quarter_hour_counts, color='skyblue', width=0.2, align='center')
    plt.xlabel('Quarter-hour of the day')
    plt.ylabel('Frequency')
    plt.title('Quarter-hourly Histogram')
    plt.xticks(range(24))
    plt.grid(True)
    plt.show()


def graph_day_of_week(pdf_text):
    days_and_hours = track_days(pdf_text, True)

    days_of_week = [datetime.strptime(dt_str, '%m/%d/%y %I:%M%p').strftime('%A') for dt_str in days_and_hours]

    day_counts = {day: days_of_week.count(day) for day in set(days_of_week)}

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Plot bar graph
    plt.figure(figsize=(10, 5))
    plt.bar(days_order, [day_counts.get(day, 0) for day in days_order], color='skyblue')
    plt.xlabel('Day of the week')
    plt.ylabel('Frequency')
    plt.title('Days of the Week Bar Graph')

    plt.grid(True)
    plt.show()


def graph_day_of_month(pdf_text):
    days_and_hours = track_days(pdf_text, True)

    days_of_month = [int(datetime.strptime(dt_str, '%m/%d/%y %I:%M%p').strftime('%d')) for dt_str in days_and_hours]

    day_counts = [days_of_month.count(day) for day in range(1, 32)]

    plt.figure(figsize=(10, 5))
    plt.bar(range(1, 32), day_counts, color='skyblue')
    plt.xlabel('Day of the Month')
    plt.ylabel('Frequency')
    plt.title('Day Histogram')
    plt.xticks(range(1, 32))
    plt.grid(True)
    plt.show()


def graph_words_scatterplot(pdf_text):
    posts = [len(post.split()) for post in get_posts(pdf_text)]
    del posts[0]

    x_values = np.arange(1, len(posts) + 1)
    y_values = posts

    slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)

    plt.scatter(x_values, y_values, label='Words', marker='o')

    plt.plot(x_values, intercept + slope * x_values, color='red',
             label=f'Line of Best Fit (slope={slope:.2f} | R^2={r_value ** 2:.2f})')

    plt.xlabel('Post Number')
    plt.ylabel('Words')
    plt.title('Words per Post')
    plt.legend()
    plt.show()


def graph_frequencies(length_list, include_labels, kind):
    length_counts = Counter(length_list)

    lengths = list(length_counts.keys())
    counts = list(length_counts.values())

    colors = ['skyblue', 'lightgreen']

    for i, (length, count) in enumerate(sorted(zip(lengths, counts))):
        plt.bar(length, count, color=colors[i % len(colors)])

    plt.xlabel(kind + ' Length')
    plt.ylabel('Frequency')
    plt.title(kind + ' Length Frequency')

    if include_labels:
        for i, count in enumerate(counts):
            plt.text(lengths[i], count + 0.1, str(count), ha='center')

    plt.show()


def graph_word_length_frequency(pdf_text, include_labels=True, max_length=12):
    word_lengths = [len(word) for word in clean_text(pdf_text).split() if len(word) <= max_length]

    graph_frequencies(word_lengths, include_labels, "Word")


def graph_sentence_length_frequency(pdf_text, include_labels=False, max_length=70):
    sentence_lengths = [len(sentence.split()) for sentence in get_sentences(pdf_text)
                        if len(sentence.split()) <= max_length]

    graph_frequencies(sentence_lengths, include_labels, "Sentence")


def graph_post_length_frequency(pdf_text, max_length=10000):
    post_lengths = [len(post.split()) for post in get_posts(pdf_text) if len(post.split()) < max_length]

    plt.hist(post_lengths, bins=50, color='skyblue', edgecolor='black')

    plt.xlabel('Post Length')
    plt.ylabel('Frequency')
    plt.title('Histogram of Post Lengths')

    plt.show()


def graph_certain_word_frequency(pdf_text, word):
    posts = get_posts(pdf_text)
    del posts[0]
    word_counts = [0] * len(posts)

    for i, post in enumerate(posts):
        word_counts[i] += len(re.findall(r'[^a-zA-Z]{}[^a-zA-Z]'.format(word), post, re.IGNORECASE))

    print(word_counts)

    x_values = list(range(len(word_counts)))

    plt.scatter(x_values, word_counts, color='skyblue')

    plt.xlabel('Post')
    plt.ylabel('Word count')
    plt.title('Scatter Plot of frequency of "{}"'.format(word))

    plt.show()
