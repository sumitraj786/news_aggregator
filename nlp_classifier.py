import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.stem import WordNetLemmatizer
import pickle  # Import the pickle module

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Sample training dataset - Replace with a real dataset
training_data = [
    ("Protesters gathered in the city center.", "Terrorism/Protest/Political Unrest/Riot"),
    ("A heartwarming story about a community coming together.", "Positive/Uplifting"),
    ("Earthquake shakes the region.", "Natural Disasters"),
    ("New technology breakthrough announced.", "Others"),
    # Add more training examples as needed
]

# Preprocess the training data
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = word_tokenize(text.lower())
    words = [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
    return dict([(word, True) for word in words])

# Apply preprocessing to the training data
processed_data = [(preprocess_text(text), category) for (text, category) in training_data]

# Train the Naive Bayes classifier
classifier = NaiveBayesClassifier.train(processed_data)

# Save the classifier to a file using pickle
with open('nlp_classifier.pickle', 'wb') as file:
    pickle.dump(classifier, file)
