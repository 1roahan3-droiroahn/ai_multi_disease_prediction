# 🏥 AI Multi-Disease Prediction

![Python](https://img.shields.io/badge/Python-3.11-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> **GTU Post Graduate Diploma in Data Science — Mini Project**
> **Student:** Pancholi Rohankumar Ashvinbhai | **Enrollment:** 251370680011

---

## 🚀 Live Demo

🔗 **https://1roahan3-droiroahn-ai-multi-disease-prediction-app-wpqa56.streamlit.app/**

---

## 📌 Problem Statement

Early and accurate disease identification is critical in healthcare. Manual diagnosis based on symptoms is time-consuming and error-prone.

**Goal:** Build an AI model that predicts one of 10 disease conditions (or Healthy) from patient vitals and symptoms using supervised machine learning.

---

## 🦠 Disease Classes

| # | Disease | Key Symptoms |
|---|---------|-------------|
| 1 | Flu | Fever + Cough + Fatigue + High Temp |
| 2 | Common Cold | Cough + Runny Nose + Sore Throat |
| 3 | Allergy | Skin Rash + Runny Nose + Headache |
| 4 | Migraine | Headache + Fatigue (no fever) |
| 5 | Food Poisoning | Nausea + Vomiting + Fatigue |
| 6 | Skin Infection | Skin Rash + Fever |
| 7 | Asthma | Wheezing + Cough |
| 8 | Hypertension Risk | High BP + Age > 40 |
| 9 | Diabetes Risk | High Glucose + Age > 35 |
| 10 | Healthy | No significant condition |

---

## 📊 Dataset

| Feature | Type | Description |
|---------|------|-------------|
| age | Numeric | Patient age (5–84) |
| sex | Categorical | Gender (male / female) |
| temperature_f | Numeric | Body temperature (°F) |
| systolic_bp | Numeric | Systolic blood pressure |
| glucose | Numeric | Blood glucose level (mg/dL) |
| cough, fever, headache... | Binary | Symptom flags (0/1) |
| predicted_disease_label | **Target** | Disease class (10 classes) |

- **Records:** 5,000 (synthetically generated)
- **Features:** 15 input features

---

## ⚙️ Methodology

```
Dataset Generation → EDA → Preprocessing → Model Training → Evaluation → Deployment
```

1. **Dataset Generation** — Rule-based synthetic data for 10 disease classes
2. **EDA** — Distribution plots, correlation heatmap, class balance
3. **Preprocessing** — One-Hot Encoding for `sex`, 80/20 train-test split
4. **Model** — Random Forest Classifier (200 trees)
5. **Evaluation** — Accuracy, Classification Report, Confusion Matrix
6. **Deployment** — Streamlit web app for live predictions

---

## 📈 Model Results

| Metric | Value |
|--------|-------|
| **Accuracy** | ~88–92% |
| **Model** | Random Forest (200 estimators) |
| **Classes** | 10 disease categories |

---

## 🗂️ Project Structure

```
ai_multi_disease_prediction/
├── app.py                              # Streamlit web application
├── ai_multi_disease_prediction.ipynb  # Full analysis notebook
├── requirements.txt                   # Dependencies
├── runtime.txt                        # Python version for Streamlit Cloud
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| pandas & NumPy | Data handling |
| scikit-learn | ML pipeline, Random Forest |
| matplotlib & seaborn | Visualizations |
| Streamlit | Web application |
| Jupyter Notebook | Analysis & report |

---

## 💻 Run Locally

```bash
git clone https://github.com/pancholi-rohan/ai_multi_disease_prediction.git
cd ai_multi_disease_prediction
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📚 References

1. scikit-learn — Random Forest Classifier
2. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1).
3. Streamlit Documentation
4. WHO — Disease Classification & Symptom Guidelines
5. GTU PGDDS Mini Project Guidelines 2025-26

---

## 👤 Author

**Pancholi Rohankumar Ashvinbhai**
Enrollment: 251370680011
Gujarat Technological University (GTU) — PGDDS Mini Project
Academic Year 2025-26, Semester-2
Internal Guide: Prof. Anamika Mittal
