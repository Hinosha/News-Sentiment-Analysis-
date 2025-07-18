import requests
import pandas as pd
import nltk
import streamlit as st

# Ensure the VADER lexicon is available
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Get API key from Streamlit secrets
def get_api_key():
    return st.secrets["goperigon_api_key"]

def fetch_news(product, api_key):
    url = (
        f"https://api.goperigon.com/v1/all?"
        f"sourceGroup=top100&apiKey={api_key}&q={product}"
        f"&from=2024-01-01&language=en"
    )
    response = requests.get(url)
    return response.json().get("articles", [])

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']

def process_articles(articles):
    df = pd.DataFrame(articles)
    df['Sentiment'] = df['content'].astype(str).apply(analyze_sentiment)
    df['Label'] = df['Sentiment'].apply(
        lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Neutral"
    )
    return df
