About Xenon
Xenon is a sophisticated, machine learning-powered chatbot designed to showcase an end-to-end conversational AI system. This project demonstrates core Natural Language Processing (NLP) capabilities, intelligent dialogue management, and advanced response generation using a Retrieval-Augmented Generation (RAG) approach, all wrapped in a clean, professional web interface.

The primary goal of Xenon is to provide users with a dynamic and contextual conversational experience, serving as a robust portfolio piece highlighting skills in building practical AI solutions.

Features
Intelligent Natural Language Understanding (NLU):

Intent Recognition: Accurately classifies user queries to understand their underlying purpose (e.g., greeting, order_status, product_info, general_info).

Sentiment Analysis: Detects the emotional tone of user messages (positive, negative, neutral) to provide more empathetic and adaptive responses.

Context-Aware Dialogue Management: Maintains conversation history and state, enabling more natural, multi-turn interactions. Basic user profiling is also implemented (e.g., remembering user's name).

Retrieval-Augmented Generation (RAG):

Leverages a custom Knowledge Base (FAQs, domain-specific information including facts about Assam, its tea, and wildlife) for grounded, factual responses.

Utilizes a Generative Language Model (GPT-2 via Hugging Face Transformers) to craft human-like and dynamic replies based on retrieved context, reducing "hallucinations" common in pure generative models.

Modular Architecture: Organized into distinct components (NLU, Dialogue Manager, Knowledge Base) for scalability and maintainability.

Professional Web Interface: A sleek and intuitive chat interface built with Flask and custom CSS, providing a polished user experience.

Error Handling: Includes basic fallbacks and "thinking" indicators for a smoother user interaction.

Technologies Used
Python 3.12 (Recommended, with PyTorch backend for Transformers compatibility)

Flask: Web framework for the backend server and API.

Hugging Face Transformers: For the generative AI pipeline (using gpt2).

PyTorch: Deep learning framework (backend for Transformers).

Scikit-learn: For classical machine learning models (e.g., LinearSVC for intent classification).

NLTK (Natural Language Toolkit): For sentiment analysis (VADER lexicon).

NumPy & Pandas: For data manipulation and numerical operations.

HTML, CSS, JavaScript: For the frontend user interface.


Setup & Installation
Follow these steps to get Xenon up and running on your local machine.

Prerequisites
Python 3.12 (Recommended): While other versions might work, this project was built with Python 3.12 leveraging PyTorch for transformers compatibility.

Important for Windows Users: If you previously faced DLL load failed errors with TensorFlow, ensure you've followed the steps to disable python.exe and python3.exe aliases in "App execution aliases" within Windows Settings (Apps > Advanced app settings) and installed Python 3.12 correctly.
Virtual Environment Setup
It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with your system's Python packages.

Bash

# Create a virtual environment
python -m venv venv_xenon

# Activate the virtual environment
# On Windows (Command Prompt):
.\venv_xenon\Scripts\activate
# On Windows (PowerShell):
# .\venv_xenon\Scripts\Activate.ps1
# On macOS/Linux:
# source venv_xenon/bin/activate
You should see (venv_xenon) prefixing your terminal prompt, indicating the environment is active.

Install Dependencies
With your virtual environment activated, install all required Python libraries:

Bash

pip install Flask scikit-learn numpy pandas nltk transformers torch accelerate
# Note: 'torch' is installed here for PyTorch backend with transformers.
# If you have an NVIDIA GPU and wish to use it, refer to the PyTorch website
# for the correct installation command (e.g., with specific CUDA versions).
NLTK Data Download
The nltk library requires the vader_lexicon for sentiment analysis. Download it once:

Bash

python -c "import nltk; nltk.download('vader_lexicon')"
How to Run
Ensure your virtual environment is active (as shown in "Virtual Environment Setup").

Navigate to the chatbot_project directory if you are not already there.

Run the Flask application:

Bash

python app.py
You should see output indicating the Flask development server has started.

How to Use
Open your web browser (Chrome, Firefox, Edge, etc.).

Go to the following address: http://127.0.0.1:5000/

The Xenon chatbot interface will appear.

Type your messages into the input field and press Enter or click the "Send" button.
