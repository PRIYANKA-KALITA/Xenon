# app.py
from flask import Flask, render_template, request, jsonify
import os
import sys

# Add parent directory to path to import modules from nlu, dialogue_manager, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'nlu')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'dialogue_manager')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'knowledge_base')))


from intent_model import predict_intent, train_intent_model
from sentiment_model import get_sentiment
from context_tracker import ContextTracker
from qa_retriever import retrieve_info, generate_response_with_context

app = Flask(__name__)
context_tracker = ContextTracker()

# Create dummy data directories and files if they don't exist
if not os.path.exists("data"):
    os.makedirs("data")
    # Dummy intents data
    dummy_intents = {
        'text': [
            "Hi there", "Hello", "Good morning", "Hey",
            "Where is my package?", "Track my order", "Order status please",
            "Tell me about product A", "What is feature B?", "Product details",
            "Thanks", "Bye", "See you later",
            "I am angry", "This service is bad", "I'm upset",
            "This is great", "I am happy", "Excellent service"
        ],
        'intent': [
            "greeting", "greeting", "greeting", "greeting",
            "order_status", "order_status", "order_status",
            "product_info", "product_info", "product_info",
            "farewell", "farewell", "farewell",
            "negative_feedback", "negative_feedback", "negative_feedback",
            "positive_feedback", "positive_feedback", "positive_feedback"
        ]
    }
    import pandas as pd
    pd.DataFrame(dummy_intents).to_csv("data/intents.csv", index=False)

if not os.path.exists("models"):
    os.makedirs("models")

# Train models on startup (or you can pre-train and load)
try:
    train_intent_model("data/intents.csv")
except Exception as e:
    print(f"Error training intent model: {e}. Make sure 'data/intents.csv' exists and is correctly formatted.")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Please type something."})

    # 1. NLU: Intent Recognition
    intent = predict_intent(user_message)

    # 2. NLU: Sentiment Analysis
    sentiment = get_sentiment(user_message)

    # (Optional) 3. NLU: Entity Extraction (Placeholder for now)
    entities = {} # In a real project, you'd have an entity extraction model here

    # 4. Knowledge Base & Retrieval
    retrieved_info = retrieve_info(intent, entities)

    # 5. Response Generation (using RAG logic)
    bot_response = generate_response_with_context(
        user_message,
        retrieved_info,
        sentiment,
        intent,
        context_tracker # Pass the context tracker instance
    )

    # 6. Dialogue Management: Update Context
    context_tracker.update_context(user_message, bot_response, intent, entities, sentiment)

    # Optional: Store user's name if they say it
    if intent == "greeting" and "my name is" in user_message.lower():
        # Very basic name extraction - use NER for robust solution
        name_parts = user_message.lower().split("my name is")
        if len(name_parts) > 1:
            name = name_parts[1].split()[0].strip().capitalize()
            context_tracker.update_user_profile("name", name)
            bot_response = f"Nice to meet you, {name}! How can I assist you today?"


    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)