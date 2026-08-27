
# 🚧 Road Safety Complaint Analyzer

An end-to-end **NLP-powered road complaint management system** that automatically analyzes citizen complaints, predicts their **category and priority**, and helps road administration efficiently identify and address critical road-related issues.

The application provides separate workflows for **users and administrators**. Users can register and submit road complaints, while administrators can monitor, categorize, prioritize, and manage complaints through an interactive dashboard.

A key feature of the system is its **continuous dataset improvement workflow**: complaints are stored in PostgreSQL and can later be reviewed by administrators. If a predicted category or priority is incorrect, the administrator can correct the labels, allowing the verified data to be reused for future model training.

---


## 🧠 NLP & Machine Learning

The system uses a traditional NLP text-classification pipeline:

Complaint Text
      ↓
Text Cleaning
(NLTK + Regular Expressions)
      ↓
TF-IDF Vectorization
(Unigrams + Bigrams)
      ↓
Multinomial Naive Bayes
      ↓
┌───────────────────┬───────────────────┐
│ Category Model    │ Priority Model    │
└─────────┬─────────┴─────────┬─────────┘
          ↓                   ↓
   Complaint Category    Priority Level
Text Preprocessing

Complaint text is preprocessed using:

Lowercasing
Regular-expression based cleaning
Tokenization
English stop-word removal using NLTK
Feature Extraction

TF-IDF (Term Frequency–Inverse Document Frequency) is used to convert the cleaned complaint text into numerical features. The model uses both unigrams and bigrams to capture individual words as well as two-word combinations.

Classification Model

The project uses Multinomial Naive Bayes, a probabilistic machine-learning algorithm well suited for text classification.

Two separate classifiers are trained:

Category Classifier — predicts the type/category of road complaint.
Priority Classifier — predicts the priority level of the complaint.

The models are trained using labeled complaint data and saved using joblib for use by the Flask application.

from sklearn.naive_bayes import MultinomialNB

category_model = MultinomialNB()
priority_model = MultinomialNB()

Model performance is evaluated using precision, recall, F1-score, and classification reports.

## ✨ Key Features

### 👤 User Management

* User registration and login
* Secure complaint submission
* Users can report road-related issues through the web application
* Complaint details are stored in the database

### 🧠 NLP-Based Complaint Classification

The system automatically analyzes the text of a submitted complaint and predicts:

* **Complaint Category**
* **Complaint Priority**

This allows road authorities to quickly understand the nature and urgency of reported problems.

### 📊 Admin Dashboard

Administrators can:

* View all submitted complaints
* Filter and analyze complaints by category
* Identify high-priority complaints
* Monitor complaint distribution
* Review individual complaints
* Correct incorrect model predictions

This enables road authorities to prioritize complaints that require immediate attention.

### 🗄️ PostgreSQL Database

All complaint records are persisted in a **PostgreSQL database**.

The database stores information such as:

* Complaint description
* Predicted category
* Predicted priority
* Corrected labels
* User/complaint information

The PostgreSQL database is **containerized using Docker**, making the development and deployment environment easier to reproduce.

### 🔄 Human-in-the-Loop Model Improvement

One of the important features of the project is the feedback mechanism between the application and the ML model.

```text
User submits complaint
        ↓
NLP model analyzes complaint
        ↓
Category + Priority predicted
        ↓
Complaint stored in PostgreSQL
        ↓
Admin reviews prediction
        ↓
Incorrect label? → Admin corrects it
        ↓
Verified complaint data
        ↓
Used as additional training data
        ↓
Model can be retrained
```

This creates a **human-in-the-loop learning workflow**, where administrator corrections can improve the quality of the training dataset and subsequently the model's predictions.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    │  Register / Login   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Flask Web App     │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                  Complaint    │
                  Text         ▼
                    ┌─────────────────────┐
                    │    NLP Classifier   │
                    │                     │
                    │ Category Prediction │
                    │ Priority Prediction │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │      Database       │
                    │                     │
                    │ Complaints + Labels │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Admin Dashboard   │
                    │                     │
                    │ Review / Correct    │
                    │ Complaints & Labels │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Verified Training   │
                    │       Data          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Model Retraining  │
                    └─────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask

### Machine Learning / NLP

* Natural Language Processing
* Text Classification
* Machine Learning model for complaint classification and priority prediction

### Database

* PostgreSQL
* SQLAlchemy / database integration

### Frontend

* HTML
* CSS
* JavaScript
* Flask/Jinja templates

### Deployment & Infrastructure

* Docker
* Dockerized PostgreSQL database
* Environment variables using `.env`

---

## 📁 Project Structure

```text
road_safety_ai/
│
├── data/
│   └── Training / dataset files
│
├── model/
│   └── Trained ML model files
│
├── static/
│   └── CSS, JavaScript and static assets
│
├── templates/
│   └── HTML templates
│
├── app.py
│   └── Flask application
│
├── models.py
│   └── Database models
│
├── extensions.py
│   └── Application/database extensions
│
├── trainmodel.py
│   └── Model training pipeline
│
├── createdataset.py
│   └── Dataset creation/preparation
│
├── lowprioritycomp.py
│   └── Complaint priority processing
│
├── complaints.csv
│   └── Complaint dataset
│
├── low_priority_complaints.csv
│   └── Low-priority complaint data
│
├── DBConnection.txt
│   └── Database connection/configuration notes
│
├── Containerization(Docker).txt
│   └── Docker setup notes
│
├── DockerInstance.docx
│   └── Docker/database documentation
│
└── requirements.txt
```

> Update the file list before publishing if your actual repository contains additional or different files.

---

## 🚀 Application Workflow

### 1. User Registration

A new user creates an account and logs into the application.

### 2. Complaint Submission

The user submits a description of a road-related issue, such as:

```text
"There is a large pothole near the main road which has become dangerous
for vehicles, especially at night."
```

### 3. NLP Analysis

The complaint text is processed by the trained NLP model.

The system predicts:

```text
Category: Pothole
Priority: High
```

### 4. Database Storage

The complaint and its prediction are stored in PostgreSQL.

### 5. Administrative Review

The administrator can view the complaint through the dashboard and monitor complaints based on their predicted category and priority.

### 6. Label Correction

If the model makes an incorrect prediction, the administrator can manually correct the category or priority.

For example:

```text
Model Prediction:
Category → Road Damage
Priority → Medium

Admin Correction:
Category → Pothole
Priority → High
```

### 7. Dataset Improvement

The corrected complaint becomes a more reliable labeled data point that can be incorporated into the training dataset.

### 8. Model Retraining

The accumulated verified complaints can be used to retrain the model and potentially improve future predictions.

---

## 🎯 Motivation

Road-related complaints are often submitted as unstructured text. Manually reading and prioritizing every complaint can be time-consuming, particularly when a large number of complaints are received.

This project demonstrates how **Natural Language Processing and Machine Learning can automate the initial classification and prioritization of road complaints**, helping authorities identify important issues more efficiently.

The administrator feedback mechanism also addresses an important real-world ML problem: **model predictions are not always correct**.

Instead of treating the model as a completely static component, the system allows human administrators to validate and correct predictions, creating a continuously improving labeled dataset.

---

## 🔄 Continuous Improvement Pipeline

The project follows a practical ML feedback loop:

```text
             ┌──────────────────┐
             │ New Complaint    │
             └────────┬─────────┘
                      ↓
             ┌──────────────────┐
             │ Model Prediction │
             └────────┬─────────┘
                      ↓
             ┌──────────────────┐
             │ Admin Validation │
             └────────┬─────────┘
                      ↓
              ┌───────┴────────┐
              │                │
           Correct          Incorrect
              │                │
              │          Admin Corrects
              │                │
              └───────┬────────┘
                      ↓
             ┌──────────────────┐
             │ Verified Dataset │
             └────────┬─────────┘
                      ↓
             ┌──────────────────┐
             │ Model Retraining │
             └──────────────────┘
```

---

## 🐳 Dockerized PostgreSQL

PostgreSQL is containerized using Docker rather than requiring PostgreSQL to be installed directly on the host machine.

This provides:

* Reproducible database setup
* Easier development environment configuration
* Isolation of database dependencies
* Easier deployment and project setup

The application connects to the PostgreSQL container through the configured database connection settings.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd road_safety_ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file containing the required application and database configuration.

Example:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
SECRET_KEY=<your-secret-key>
```

**Do not commit your `.env` file or database credentials to GitHub.**

### 5. Start PostgreSQL

Start the PostgreSQL Docker container using the project's Docker configuration.

```bash
docker ps
```

Verify that the PostgreSQL container is running.

### 6. Run the Flask Application

```bash
python app.py
```

Open the application in your browser at:

```text
http://127.0.0.1:5000
```

---

## 🧪 Model Training

The project includes a training pipeline that can be used to train/retrain the complaint classification model using the available labeled dataset.

```bash
python trainmodel.py
```

The training workflow can incorporate administrator-verified complaint records to improve the dataset used for future model training.

---

## 📌 Future Improvements

Potential improvements include:

* More advanced transformer-based NLP models
* Better handling of multilingual complaints
* Real-time complaint analytics
* Geolocation-based complaint mapping
* Automatic duplicate complaint detection
* Model performance monitoring
* Confidence scores for predictions
* Automated retraining pipelines
* REST API for integration with other road-management systems
* Dockerizing the complete application
* Cloud deployment
* Role-based access control for administrators

---

## 💡 Project Highlights

* End-to-end **NLP + Web Application**
* Automated complaint **classification and prioritization**
* **Human-in-the-loop** feedback mechanism
* Persistent complaint storage using **PostgreSQL**
* **Dockerized database infrastructure**
* Admin dashboard for complaint management
* Retraining workflow using verified complaint data
* Practical application of ML to a real-world civic problem

---

## 👨‍💻 Project Objective

The primary objective of this project is to demonstrate how an NLP-based machine learning system can be integrated into a real-world application to automatically analyze citizen complaints, prioritize road maintenance issues, and create a feedback-driven mechanism for improving future predictions.
