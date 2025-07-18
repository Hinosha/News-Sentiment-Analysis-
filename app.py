import streamlit as st
import pandas as pd
from sentiment_analysis import process_articles

st.set_page_config(page_title="Product News Sentiment Analyzer", layout="centered")

st.markdown("## 📰 Product News Sentiment Analyzer")

# Input UI
query = st.text_input("Enter a product or keyword to analyze", "Apple")
days = st.slider("Number of days to analyze", 1, 30, 7)

if st.button("Analyze News"):
    try:
        api_token = st.secrets["api_token"]
        base_url = st.secrets["base_url"]

        with st.spinner("Fetching and analyzing news..."):
            articles_df, sentiment_df = process_articles(api_token, base_url, query, days)

        st.success("Analysis completed!")

        st.subheader("📊 Sentiment Summary")
        st.dataframe(sentiment_df)

        st.subheader("🗞️ News Articles")
        st.dataframe(articles_df[["Date", "Title", "Content"]])

        # Option to download CSVs
        csv_sentiment = sentiment_df.to_csv(index=False).encode('utf-8')
        csv_articles = articles_df.to_csv(index=False).encode('utf-8')

        st.download_button("Download Sentiment CSV", csv_sentiment, f"{query}_sentiment.csv", "text/csv")
        st.download_button("Download Articles CSV", csv_articles, f"{query}_articles.csv", "text/csv")

    except Exception as e:
        st.error(f"An error occurred: {e}")
