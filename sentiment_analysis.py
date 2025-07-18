import requests
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import streamlit as st

nltk.download('vader_lexicon')

def get_api_key():
    return st.secrets["goperigon_api_key"]

def fetch_news(product, api_key):
    url = f"https://api.goperigon.com/v1/all?sourceGroup=top100&apiKey={api_key}&q={product}&from=2024-01-01&language=en"
    response = requests.get(url)
    return response.json().get("articles", [])

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']

def process_articles(articles):
    df = pd.DataFrame(articles)
    df['Sentiment'] = df['content'].astype(str).apply(analyze_sentiment)
    df['Label'] = df['Sentiment'].apply(lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Neutral")
    return df
