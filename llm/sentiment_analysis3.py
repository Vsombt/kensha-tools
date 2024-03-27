from transformers import pipeline
import pandas as pd

# Load your messages DataFrame
df = pd.read_csv('data/messages.csv')

# Load a pre-trained sentiment analysis pipeline
nlp = pipeline("sentiment-analysis")

def analyze_sentiment_with_transformers(text):
    # Applying try-except to handle any potential errors with specific messages
    try:
        result = nlp(text)
        # The pipeline returns a list of dicts with 'label' and 'score'
        return result[0]['label'], result[0]['score']
    except Exception as e:
        print(f"Error processing text: {text} | Error: {e}")
        return None, None

# Apply the sentiment analysis to each message
# This operation can be slow for large datasets
df[['sentiment_label', 'sentiment_score']] = df['message'].apply(
    lambda x: pd.Series(analyze_sentiment_with_transformers(x))
)

# Now, df includes sentiment labels and scores for each message
print(df.columns)