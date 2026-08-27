from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load models
category_model = joblib.load("model/category_model.pkl")
priority_model = joblib.load("model/priority_model.pkl")
vectorizer = joblib.load("model/tfidf.pkl")

@app.route("/")
def home():
    return render_template("user.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form["complaint"]

    X = vectorizer.transform([text])

    category = category_model.predict(X)[0]
    priority = priority_model.predict(X)[0]

    # Save complaint
    file_path = "data/complaints_log.csv"
    row = pd.DataFrame([[text, category, priority]],
                       columns=["complaint", "category", "priority"])

    if os.path.exists(file_path):
        row.to_csv(file_path, mode="a", header=False, index=False)
    else:
        row.to_csv(file_path, index=False)

    return render_template(
        "result.html",
        complaint=text,
        category=category,
        priority=priority
    )


@app.route("/admin")
def admin():
    df = pd.read_csv("data/complaints_log.csv")

    category_count = df["category"].value_counts().to_dict()
    priority_count = df["priority"].value_counts().to_dict()

    return render_template(
        "admin.html",
        tables=df.to_html(index=False),
        category_count=category_count,
        priority_count=priority_count
    )


if __name__ == "__main__":
    app.run(debug=True)
