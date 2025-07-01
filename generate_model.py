import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])

# Clean messages
def clean_message(msg):
    msg = msg.lower()
    msg = msg.translate(str.maketrans('', '', string.punctuation))
    return msg

df['cleaned_message'] = df['message'].apply(clean_message)

# Vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['cleaned_message'])
y = df['label'].apply(lambda x: 1 if x == 'spam' else 0)

# Train model
model = MultinomialNB()
model.fit(X, y)

# Save the model and vectorizer
with open('model/spam_classifier.pkl', 'wb') as f:
    pickle.dump((model, vectorizer), f)

print("✅ spam_classifier.pkl saved successfully.")
