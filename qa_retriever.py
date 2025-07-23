# knowledge_base/qa_retriever.py
import os
from transformers import pipeline, set_seed
import random

# A very simple "knowledge base" - in a real project, this would be a database, Faiss index, etc.
KNOWLEDGE_BASE = {
    "order_status": "To check your order status, please provide your order ID.",
    "product_A_info": "Product A is our latest gadget with XYZ features and costs $199.",
    "product_B_info": "Product B is an accessory for Product A, enhancing its battery life.",
    "shipping": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days.",
    "returns": "You can return items within 30 days for a full refund. Please visit our returns policy page.",
    "contact_support": "You can contact support at support@example.com or call us at 1-800-BOT-HELP."
}

# Initialize a simple text generation pipeline (e.g., using GPT-2 for demonstration)
# Explicitly set the device to 'cpu' and the framework to 'pt' (PyTorch)
try:
    generator = pipeline(
        'text-generation',
        model='gpt2',
        device='cpu', # Force CPU usage if no GPU is preferred/available
        framework='pt' # Explicitly use PyTorch backend
    )
except Exception as e:
    print(f"Could not load GPT-2 model or pipeline (requires ~500MB download): {e}")
    print("Proceeding without a generative model. Responses will be purely retrieval-based.")
    generator = None # Fallback

set_seed(42)

def retrieve_info(intent, entities=None):
    # This is a very basic retrieval based on intent.
    # In a real system, you'd use semantic search, embeddings, etc.
    if intent == "order_status":
        return KNOWLEDGE_BASE.get("order_status")
    elif intent == "product_info":
        # You'd use 'entities' here to find specific product info
        if entities and "product_A" in entities: # Assume entity extraction found "product_A"
            return KNOWLEDGE_BASE.get("product_A_info")
        elif entities and "product_B" in entities:
             return KNOWLEDGE_BASE.get("product_B_info")
        else:
            return "Can you specify which product you are interested in?"
    elif intent == "shipping_info":
        return KNOWLEDGE_BASE.get("shipping")
    elif intent == "return_policy":
        return KNOWLEDGE_BASE.get("returns")
    elif intent == "contact_us":
        return KNOWLEDGE_BASE.get("contact_support")
    return None

def generate_response_with_context(user_query, retrieved_context, sentiment, intent, context_tracker):
    # Use retrieved context and potentially generative model
    response = ""
    user_profile = context_tracker.get_user_profile()
    user_name = user_profile.get("name", "there")

    # --- Rule-based responses based on intent and sentiment ---
    if intent == "greeting":
        greetings = ["Hello!", "Hi!", "Hey!", "Greetings!"]
        if sentiment == "positive":
            response = f"{random.choice(greetings)} It's great to hear from you, {user_name}!"
        else:
            response = f"{random.choice(greetings)} How can I assist you today, {user_name}?"
    elif intent == "farewell":
        farewells = ["Goodbye!", "See you!", "Talk to you later!"]
        response = random.choice(farewells)
    elif sentiment == "negative":
        # If user is negative, try to offer help or escalate
        response = "I apologize if you're having a bad experience. How can I help resolve this?"
        if intent not in ["contact_us", "order_status"]: # Avoid redundancy
            response += " Would you like me to connect you with a human agent?"
    elif sentiment == "positive":
        response = f"That's great to hear! How else can I help, {user_name}?"


    # --- RAG part: Combine retrieved info with generative model ---
    if retrieved_context:
        if generator:
            # This is a *simplified* RAG. Real RAG involves feeding context effectively into LLM.
            prompt = f"User asked: '{user_query}'. Relevant information: '{retrieved_context}'. Based on this information, provide a concise and helpful answer."
            try:
                generated_text = generator(prompt, max_new_tokens=50, num_return_sequences=1,
                                        no_repeat_ngram_size=2,
                                        eos_token_id=generator.tokenizer.eos_token_id)[0]['generated_text']
                # Post-process to get just the answer part if the LLM adds the prompt
                response = generated_text.replace(prompt, "").strip()
                if not response: # Fallback if generator struggles
                    response = retrieved_context
            except Exception as e:
                print(f"Error during text generation: {e}")
                response = retrieved_context # Fallback to just retrieved text
        else:
            response = retrieved_context
    elif not response: # If no specific rule-based or retrieved response, provide a generic answer
        response = "I'm not sure I understand. Can you rephrase that or ask a different question?"

    return response

# Example of how you might call it
# retrieved_data = retrieve_info(intent_predicted, entities_extracted)
# bot_response = generate_response_with_context(user_input, retrieved_data, sentiment_predicted, intent_predicted, context_tracker)