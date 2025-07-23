# nlu/sentiment_model.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# It's generally best practice to ensure NLTK data is present
# by asking the user to run nltk.download() separately.
# However, if you want to try to download it if missing, you can
# use a simpler approach or rely on NLTK's internal checks.

# Let's simplify this section, as the direct `nltk.downloader.DownloadError`
# is causing an AttributeError. The LookupError is caught by NLTK itself.
# The most common way is to simply attempt to use it, and let NLTK raise
# the LookupError with clear instructions if not found, or to explicitly
# download it at the script's entry point (e.g., in app.py or a setup script).

# We'll remove the try-except for DownloadError here, as it's not the standard way
# to handle missing NLTK resources within a module. The primary issue is
# that the 'vader_lexicon' itself is missing.

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    vs = analyzer.polarity_scores(text)
    # Classify based on compound score
    if vs['compound'] >= 0.05:
        return "positive"
    elif vs['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

if __name__ == "__main__":
    # This block is for testing the sentiment model directly.
    # It will attempt to load the analyzer, which requires the lexicon.
    # If the lexicon is not downloaded, it will raise a LookupError.
    # So, ensure you've run nltk.download('vader_lexicon') before this.
    print(f"'I love this product!' sentiment: {get_sentiment('I love this product!')}")
    print(f"'This is terrible service.' sentiment: {get_sentiment('This is terrible service.')}")
    print(f"'The weather is fine.' sentiment: {get_sentiment('The weather is fine.')}")