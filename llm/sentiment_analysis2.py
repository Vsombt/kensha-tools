from textblob import TextBlob
import pandas as pd

# Assuming you have a DataFrame 'df' with a column 'message'
df = pd.read_csv('data/messages.csv')  # Load your messages

def analyze_detailed_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment

# Apply detailed sentiment analysis to each message
df['detailed_sentiment'] = df['message'].apply(lambda x: analyze_detailed_sentiment(x))

# Splitting the detailed sentiment into separate columns for easier analysis
df['polarity'] = df['detailed_sentiment'].apply(lambda x: x.polarity)
df['subjectivity'] = df['detailed_sentiment'].apply(lambda x: x.subjectivity)

# Now df includes polarity and subjectivity scores for each message
df = df[df['polarity'] != 0]
print(df.columns)