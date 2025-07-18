📰 News Sentiment Analysis App

This Streamlit web app allows users to:
- Select or enter a **product name**
- Fetch related **news articles** using the [GoPerigon News API](https://docs.goperigon.com/)
- Perform **sentiment analysis** using **VADER (NLTK)**
- View sentiment scores and visualizations directly on the web


🚀 Live App

🔗 [Visit the Streamlit App](https://your-streamlit-url.streamlit.app)  
*(Update this after deployment)*


📦 Features

- 🔍 Fetches real-time news articles by product keyword
- 🤖 Performs sentiment analysis using `nltk.sentiment.SentimentIntensityAnalyzer`
- 📊 Displays results in a dynamic table and sentiment distribution chart
- 🌐 Ready to deploy via Streamlit Cloud



🧪 Example Use Case

- Enter: `Tesla`
- The app fetches news about Tesla, analyzes sentiment, and shows a summary of positivity or negativity in news coverage.



🛠️ Installation (Local Use)


git clone https://github.com/yourusername/sentiment_app.git
cd sentiment_app
pip install -r requirements.txt
