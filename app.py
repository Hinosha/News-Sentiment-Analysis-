import streamlit as st
from sentiment_analysis import get_api_key, fetch_news, process_articles

st.set_page_config(page_title="News Sentiment Analyzer", layout="wide")
st.title("📰 Product News Sentiment Analyzer")

product = st.selectbox("Select a product or enter your own:", ["Apple", "Microsoft", "Tesla", "Custom"])

if product == "Custom":
    product = st.text_input("Enter your custom product name:")

if st.button("Analyze News") and product:
    with st.spinner("Fetching and analyzing..."):
        try:
            api_key = get_api_key()
            articles = fetch_news(product, api_key)
            if not articles:
                st.warning("No news articles found.")
            else:
                df = process_articles(articles)
                st.success("News articles analyzed!")
                st.dataframe(df[['title', 'publishedAt', 'Sentiment', 'Label']], use_container_width=True)
                st.bar_chart(df['Label'].value_counts())
        except Exception as e:
            st.error(f"An error occurred: {e}")
