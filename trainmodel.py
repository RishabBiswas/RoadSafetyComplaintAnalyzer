import pandas as pd
import joblib
import nltk
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

nltk.download("stopwords")
from nltk.corpus import stopwords

# ----------------------------
# Text Cleaning Function
# ----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [w for w in words if w not in stopwords.words("english")]
    return " ".join(words)

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("data/complaints.csv")

df["clean_text"] = df["complaint_text"].apply(clean_text)

# ----------------------------
# TF-IDF Vectorization
# ----------------------------
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X = vectorizer.fit_transform(df["clean_text"])

# =========================================================
# 1️⃣ CATEGORY CLASSIFICATION MODEL
# =========================================================
y_category = df["category"]

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X, y_category, test_size=0.2, random_state=42
)

category_model = MultinomialNB()
category_model.fit(X_train_c, y_train_c)

print("\n📊 CATEGORY MODEL PERFORMANCE\n")
print(classification_report(y_test_c, category_model.predict(X_test_c)))

# Save category model
joblib.dump(category_model, "model/category_model.pkl")

# =========================================================
# 2️⃣ PRIORITY CLASSIFICATION MODEL
# =========================================================
y_priority = df["priority"]

X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X, y_priority, test_size=0.2, random_state=42
)

priority_model = MultinomialNB()
priority_model.fit(X_train_p, y_train_p)

print("\n📊 PRIORITY MODEL PERFORMANCE\n")
print(classification_report(y_test_p, priority_model.predict(X_test_p)))

# Save priority model
joblib.dump(priority_model, "model/priority_model.pkl")

# ----------------------------
# Save Vectorizer
# ----------------------------
joblib.dump(vectorizer, "model/tfidf.pkl")

print("\n✅ Models and vectorizer saved successfully!")
