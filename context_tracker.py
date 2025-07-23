# dialogue_manager/context_tracker.py
class ContextTracker:
    def __init__(self):
        self.history = []  # List of (user_message, bot_response) tuples
        self.current_context = {} # Dictionary to store slots, intent, sentiment of current turn
        self.user_profile = {} # Persistent user data (e.g., name, preferences)

    def update_context(self, user_message, bot_response, intent, entities, sentiment):
        self.history.append({"user": user_message, "bot": bot_response})
        self.current_context = {
            "last_intent": intent,
            "extracted_entities": entities, # More complex: entity extraction not covered here, but would be integrated
            "last_sentiment": sentiment,
            "last_user_message": user_message
        }
        # Keep history to a reasonable length
        if len(self.history) > 10: # Keep last 5 turns for user, 5 for bot
            self.history = self.history[-10:]

    def get_current_context(self):
        return self.current_context

    def get_chat_history(self):
        return self.history

    def update_user_profile(self, key, value):
        self.user_profile[key] = value

    def get_user_profile(self):
        return self.user_profile

# Example usage in a main app file:
# context_tracker = ContextTracker()
# context_tracker.update_context("hello", "hi", "greeting", {}, "positive")
# print(context_tracker.get_current_context())