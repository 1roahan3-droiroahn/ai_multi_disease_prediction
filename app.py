import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

st.set_page_config(
    page_title="AI Multi-Disease Prediction",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e40af;
        text-align: center;
        padding: 1rem 0 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    .result-disease {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .result-label {
        font-size: 1rem;
        opacity: 0.85;
        margin-bottom: 0.3rem;
    }
    div.stButton > button {
        background-color: #16a34a;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #15803d;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def train_model():
    np.random.seed(42)
    n = 5000
    age = np.random.randint(5, 85, n)
    sex = np.random.choice(['male', 'female'], n)
    temperature_f = np.round(np.random.normal(98.6, 1.3, n), 1)
    systolic_bp = np.random.randint(95, 185, n)
    glucose = np.random.randint(70, 240, n)
    cough = np.random.binomial(1, 0.35, n)
    fever = np.random.binomial(1, 0.33, n)
    headache = np.random.binomial(1, 0.30, n)
    fatigue = np.random.binomial(1, 0.30, n)
    runny_nose = np.random.binomial(1, 0.28, n)
    sore_throat = np.random.binomial(1, 0.26, n)
    nausea = np.random.binomial(1, 0.18, n)
    vomiting = np.random.binomial(1, 0.12, n)
    skin_rash = np.random.binomial(1, 0.11, n)
    wheezing = np.random.binomial(1, 0.10, n)

    disease = []
    for i in range(n):
        if fever[i] and cough[i] and fatigue[i] and temperature_f[i] > 100.0:
            disease.append('Flu')
        elif cough[i] and runny_nose[i] and sore_throat[i] and temperature_f[i] < 100.0:
            disease.append('Common Cold')
        elif skin_rash[i] and runny_nose[i] and headache[i]:
            disease.append('Allergy')
        elif headache[i] and fatigue[i] and not fever[i] and not cough[i]:
            disease.append('Migraine')
        elif nausea[i] and vomiting[i] and fatigue[i]:
            disease.append('Food Poisoning')
        elif skin_rash[i] and fever[i] and not cough[i]:
            disease.append('Skin Infection')
        elif wheezing[i] and cough[i]:
            disease.append('Asthma')
        elif systolic_bp[i] > 160 and age[i] > 40:
            disease.append('Hypertension Risk')
        elif glucose[i] > 200 and age[i] > 35:
            disease.append('Diabetes Risk')
        else:
            disease.append('Healthy')

    df = pd.DataFrame({
        'age': age, 'sex': sex, 'temperature_f': temperature_f,
        'systolic_bp': systolic_bp, 'glucose': glucose,
        'cough': cough, 'fever': fever, 'headache': headache,
        'fatigue': fatigue, 'runny_nose': runny_nose,
        'sore_throat': sore_throat, 'nausea': nausea,
        'vomiting': vomiting, 'skin_rash': skin_rash,
        'wheezing': wheezing, 'predicted_disease_label': disease
    })

    X = df.drop('predicted_disease_label', axis=1)
    y = df['predicted_disease_label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ct = ColumnTransformer([('ohe', OneHotEncoder(handle_unknown='ignore'), ['sex'])],
                           remainder='passthrough')
    model = Pipeline([('preprocess', ct),
                      ('clf', RandomForestClassifier(n_estimators=200, random_state=42))])
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    return model, acc


model, accuracy = train_model()

st.markdown('<div class="main-header">🏥 AI Multi-Disease Prediction</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">GTU PGDDS Mini Project — Pancholi Rohankumar Ashvinbhai (251370680011)</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Model", "Random Forest")
col2.metric("Accuracy", f"{accuracy*100:.1f}%")
col3.metric("Training Records", "4,000")
col4.metric("Disease Classes", "10")

st.markdown("---")
st.subheader("Enter Patient Details")

c1, c2 = st.columns(2)
with c1:
    age = st.slider("Age", 5, 84, 35)
    temperature_f = st.slider("Body Temperature (°F)", 93.8, 103.0, 98.6, step=0.1)
    systolic_bp = st.slider("Systolic Blood Pressure (mmHg)", 95, 184, 120)
    glucose = st.slider("Glucose Level (mg/dL)", 70, 239, 110)
    sex = st.selectbox("Sex", ["male", "female"])

with c2:
    st.markdown("**Symptoms (check all that apply)**")
    cough = int(st.checkbox("Cough"))
    fever = int(st.checkbox("Fever"))
    headache = int(st.checkbox("Headache"))
    fatigue = int(st.checkbox("Fatigue"))
    runny_nose = int(st.checkbox("Runny Nose"))
    sore_throat = int(st.checkbox("Sore Throat"))
    nausea = int(st.checkbox("Nausea"))
    vomiting = int(st.checkbox("Vomiting"))
    skin_rash = int(st.checkbox("Skin Rash"))
    wheezing = int(st.checkbox("Wheezing"))

st.markdown("")
if st.button("Estimate Prediction"):
    input_df = pd.DataFrame([{
        'age': age, 'sex': sex, 'temperature_f': temperature_f,
        'systolic_bp': systolic_bp, 'glucose': glucose,
        'cough': cough, 'fever': fever, 'headache': headache,
        'fatigue': fatigue, 'runny_nose': runny_nose,
        'sore_throat': sore_throat, 'nausea': nausea,
        'vomiting': vomiting, 'skin_rash': skin_rash,
        'wheezing': wheezing
    }])

    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]
    confidence = round(max(proba) * 100, 1)

    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Predicted Condition</div>
        <div class="result-disease">{prediction}</div>
        <div style="margin-top:0.5rem; font-size:1rem;">Confidence: {confidence}%</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Input Summary"):
        st.write(input_df)

    disease_info = {
        "Flu": "Rest, hydration, and antiviral medication if needed. Consult a doctor.",
        "Common Cold": "Rest, fluids, and over-the-counter cold remedies.",
        "Allergy": "Avoid triggers. Antihistamines may help. Consult a doctor.",
        "Migraine": "Rest in a dark quiet room. Pain relievers may help.",
        "Food Poisoning": "Stay hydrated. Seek medical attention if severe.",
        "Skin Infection": "Keep the area clean. Topical or oral antibiotics may be needed.",
        "Asthma": "Use prescribed inhalers. Avoid known triggers.",
        "Hypertension Risk": "Reduce salt intake, exercise regularly. Monitor BP.",
        "Diabetes Risk": "Control diet, exercise, and monitor glucose levels.",
        "Healthy": "No significant condition detected. Maintain a healthy lifestyle!"
    }
    st.info(f"**Recommendation:** {disease_info.get(prediction, 'Consult a healthcare professional.')}")

st.markdown("---")
st.caption("Educational tool only — Not a substitute for professional medical diagnosis.")
