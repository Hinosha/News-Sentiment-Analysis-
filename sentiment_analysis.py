import re
import time
import requests
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

import streamlit as st

api_token = st.secrets["api_token"]
base_url = st.secrets["base_url"]


# Download VADER lexicon if not already available
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def fetch_news(api_token, base_url, start_date, end_date, query):
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    params = {
        'q': query,
        'from': start_date,
        'to': end_date,
        'language': 'en',
        'sort': 'date',
        'size': 100
    }
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get('articles', [])
    elif response.status_code == 400:
        print(f"Bad Request: Check parameters for {start_date} to {end_date}. Response: {response.json()}")
        return []
    elif response.status_code == 402:
        print("Payment Required: You have exceeded your free tier usage limits or need to upgrade your plan.")
        return []
    else:
        print(f"Failed to fetch news for {start_date} to {end_date}: {response.status_code}")
        return []

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def process_articles(api_token, base_url, query, days):
    start_date = datetime.now() - timedelta(days=days)
    end_date = datetime.now()

    sentiment_columns = ["Date", "News", "Positive", "Neutral", "Negative", "Final Sentiment"]
    articles_df = pd.DataFrame(columns=["Date", "Title", "Content", "Sentiment"])
    sentiment_df = pd.DataFrame(columns=sentiment_columns)

    current_date = start_date

    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        articles = fetch_news(api_token, base_url, current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'), query)
        for article in articles:
            content = article['content'] if article['content'] else article.get('summary', '')
            if content and 'pubDate' in article:
                content_clean = clean_text(content)
                scores = sia.polarity_scores(content_clean)
                final_sentiment = scores['pos'] - scores['neg']
                article_row = {
                    "Date": article['pubDate'][:10],
                    "Title": article['title'],
                    "Content": content_clean,
                    "Sentiment": final_sentiment
                }
                sentiment_row = {
                    "Date": article['pubDate'][:10],
                    "News": content_clean,
                    "Positive": scores['pos'],
                    "Neutral": scores['neu'],
                    "Negative": scores['neg'],
                    "Final Sentiment": final_sentiment
                }
                articles_df = pd.concat([articles_df, pd.DataFrame([article_row])], ignore_index=True)
                sentiment_df = pd.concat([sentiment_df, pd.DataFrame([sentiment_row])], ignore_index=True)

        current_date = next_date
        time.sleep(1)

    return articles_df, sentiment_df
