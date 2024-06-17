import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils import get_posts, graph_smooth

nlp = spacy.load('en_core_web_lg')
analyzer = SentimentIntensityAnalyzer()


def analyze(text):
    # Tokenize the text using spaCy
    doc = nlp(text[:100000])

    # Initialize variables to accumulate sentiment scores
    compound_score = 0.0
    num_sentences = 0

    # Analyze sentiment for each sentence in the text
    for sentence in doc.sents:
        # Get the sentiment scores from VADER
        # Accumulate compound score (normalized sentiment score)
        compound_score += analyzer.polarity_scores(sentence.text)['compound']
        num_sentences += 1

    # Normalize the compound score
    return compound_score / num_sentences


def analyze_overall_sentiment(pdf_text):
    score = analyze(pdf_text)

    print(f'Overall Sentiment: {score}')
    print()


def analyze_post_sentiment(pdf_text):
    posts = get_posts(pdf_text)
    del posts[0]

    scores = []

    for post in posts:
        scores.append(analyze(post))

    graph_smooth(scores, "Sentiment by post")


def analyze_sentiment_by_time(pdf_text, month=True):
    pass
