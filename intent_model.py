# nlu/intent_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
import joblib

def train_intent_model(data_path="data/intents.csv"):
    # Example data: CSV with columns 'text', 'intent'
    # e.g., "Hello there", "greeting"
    # "Where is my order", "order_status"
    df = pd.read_csv(data_path)

    X = df['text']
    y = df['intent']

    # Create a pipeline: TF-IDF for text features, then Linear SVC classifier
    model = make_pipeline(TfidfVectorizer(), LinearSVC(random_state=42))
    model.fit(X, y)

    joblib.dump(model, "models/intent_classifier.pkl")
    print("Intent model trained and saved.")
    return model

def predict_intent(text):
    model = joblib.load("models/intent_classifier.pkl")
    return model.predict([text])[0]

if __name__ == "__main__":
    # Create a dummy dataset for demonstration
    dummy_data = {
        'text': [
            "Hi there", "Hello", "Good morning", "Hey",
            "Where is my package?", "Track my order", "Order status please",
            "Tell me about product A", "What is feature B?", "Product details",
            "Thanks", "Bye", "See you later"
        ],
        'intent': [
            "greeting", "greeting", "greeting", "greeting",
            "order_status", "order_status", "order_status",
            "product_info", "product_info", "product_info",
            "farewell", "farewell", "farewell"
        ]
    }
    pd.DataFrame(dummy_data).to_csv("data/intents.csv", index=False)
    train_intent_model("data/intents.csv")
    print(f"Predicted intent for 'track my delivery': {predict_intent('track my delivery')}")