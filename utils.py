import re
from datetime import datetime
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import numpy as np

# Update this whenever you cross the International Date Line in the Eastward direction and post on both sides
ALLOWED_ERROR_HOURS = 1


def get_posts(pdf_text):
    return re.split(r"\b\d{1,2}/\d{1,2}/\d{2} \d{1,2}:\d{2}[AP]M\b", pdf_text)


def clean_text(pdf_text):
    pdf_text = pdf_text.lower()
    characters_to_be_replaced = '''.?!,'’()"“”:$-�%/\\*#=+;[]>{}@~^'''
    for char in characters_to_be_replaced:
        pdf_text = pdf_text.replace(char, "")
    return pdf_text


def track_days(pdf_text, time=False):
    if time:
        return re.findall(r"\b\d{1,2}/\d{1,2}/\d{2} \d{1,2}:\d{2}[AP]M\b", pdf_text)
    return re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', pdf_text)


def get_sentences(pdf_text):
    pdf_text = pdf_text.lower()
    pdf_text = pdf_text.replace("mr.", "mr")
    pdf_text = pdf_text.replace("mrs.", "mrs")
    pdf_text = pdf_text.replace("ms.", "ms")
    pdf_text = pdf_text.replace("vol.", "vol")

    return re.split(r'(?<=\w[.!?][\s\n])(?=[\w\n])', pdf_text)


def make_dictionary():
    with open('./dictionary.txt') as file:
        return set([line.strip() for line in file])


def days_helper(pdf_text):
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

    return date_differences


def hours_helper(pdf_text):
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

    return hour_differences


def graph_smooth(y, label):
    y = np.array(y)
    x = np.arange(len(y))

    x_smooth = np.linspace(x.min(), x.max(), 300)
    spl = make_interp_spline(x, y, k=3)  # Cubic spline
    y_smooth = spl(x_smooth)

    plt.plot(x_smooth, y_smooth, label=label, linestyle='-')

    # Add titles and labels
    plt.title(label)
    plt.xlabel('Index')
    plt.ylabel('Value')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()
