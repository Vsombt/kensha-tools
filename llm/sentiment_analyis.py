import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure the nltk VADER lexicon is available
nltk.download('vader_lexicon')

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(text)
    return sentiment_score['compound']

# Assuming you have a DataFrame 'df' with messages and corresponding senders
df = pd.read_csv('data/messages.csv')

# Analyze sentiment of each message
df['sentiment'] = df['message'].apply(analyze_sentiment)
df = df[df['sentiment'] != 0]

# Creating one boxplot per sender
plt.figure(figsize=(12, 8))
sns.boxplot(x='sentiment', y='sender', data=df, orient='h')
plt.title('Distribution of Sentiment Scores by Sender')
plt.xlabel('Sentiment Score')
plt.ylabel('Sender')
plt.tight_layout()  # Adjust layout to not cut off labels
plt.show()