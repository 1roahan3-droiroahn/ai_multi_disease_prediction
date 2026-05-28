from fpdf import FPDF
import os

OUTPUT = "251370680011_Rohan_Project_Poster.pdf"

def safe(text):
    replacements = {
        '\u2014': '-', '\u2013': '-', '\u2019': "'", '\u2018': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '*', '\u2192': '->',
        '\u00b2': '2', '\u00b0': 'deg', '\u00e9': 'e', '\u00e0': 'a',
        '\u03b1': 'alpha', '\u03b2': 'beta', '\u2248': '~', '\u2265': '>=',
        '\u2264': '<=',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')


class Poster(FPDF):
    def header(self):
        pass
    def footer(self):
        pass


pdf = Poster(orientation='P', unit='mm', format='A3')
pdf.add_page()
pdf.set_auto_page_break(False)

W = 297
H = 420

# ── Background ──────────────────────────────────────────────────────────────
pdf.set_fill_color(245, 247, 252)
pdf.rect(0, 0, W, H, 'F')

# ── Top banner ───────────────────────────────────────────────────────────────
pdf.set_fill_color(15, 52, 96)
pdf.rect(0, 0, W, 38, 'F')

pdf.set_fill_color(37, 99, 235)
pdf.rect(0, 38, W, 6, 'F')

# GTU title
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica', 'B', 14)
pdf.set_xy(0, 6)
pdf.cell(W, 8, safe('GUJARAT TECHNOLOGICAL UNIVERSITY'), align='C')
pdf.set_font('Helvetica', '', 10)
pdf.set_xy(0, 14)
pdf.cell(W, 6, safe('Post Graduate Diploma in Data Science (PGDDS)'), align='C')
pdf.set_xy(0, 20)
pdf.cell(W, 6, safe('Mini Project (DS02080041)  |  Academic Year 2025-26, Semester-2'), align='C')
pdf.set_xy(0, 27)
pdf.set_font('Helvetica', 'B', 11)
pdf.cell(W, 6, safe('Internal Guide: Prof. Anamika Mittal  |  Institute Code: 137'), align='C')

# ── Project title ────────────────────────────────────────────────────────────
pdf.set_fill_color(37, 99, 235)
pdf.rect(0, 44, W, 22, 'F')
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica', 'B', 26)
pdf.set_xy(0, 47)
pdf.cell(W, 12, safe('AI Multi-Disease Prediction'), align='C')
pdf.set_font('Helvetica', '', 13)
pdf.set_xy(0, 59)
pdf.cell(W, 7, safe('Pancholi Rohankumar Ashvinbhai  |  Enrollment: 251370680011'), align='C')

# ── Helper functions ──────────────────────────────────────────────────────────
def section_header(x, y, w, title, r=15, g=52, b=96):
    pdf.set_fill_color(r, g, b)
    pdf.rect(x, y, w, 9, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_xy(x + 3, y + 1)
    pdf.cell(w - 6, 7, safe(title))

def card(x, y, w, h, r=255, g=255, b=255, border_r=37, border_g=99, border_b=235):
    pdf.set_fill_color(r, g, b)
    pdf.set_draw_color(border_r, border_g, border_b)
    pdf.set_line_width(0.4)
    pdf.rect(x, y, w, h, 'FD')

def body_text(x, y, w, lines, size=9.5, color=(50, 50, 60)):
    pdf.set_text_color(*color)
    pdf.set_font('Helvetica', '', size)
    for line in lines:
        pdf.set_xy(x, y)
        pdf.multi_cell(w, 5.2, safe(line))
        y += 5.2

def bullet(x, y, w, items, size=9.5):
    pdf.set_text_color(40, 40, 55)
    pdf.set_font('Helvetica', '', size)
    for item in items:
        pdf.set_xy(x, y)
        pdf.cell(4, 5, '*')
        pdf.set_xy(x + 4, y)
        pdf.multi_cell(w - 4, 5, safe(item))
        y += 5.2
    return y

# ════════════════════════════════════════════════════════════════════════════
# ROW 1  (y=72)
# ════════════════════════════════════════════════════════════════════════════
margin = 8
col_w = (W - 3 * margin) / 2
row1_y = 72

# ── Problem Statement (left) ─────────────────────────────────────────────────
card(margin, row1_y, col_w, 68)
section_header(margin, row1_y, col_w, '  PROBLEM STATEMENT')
body_text(margin + 4, row1_y + 12, col_w - 8, [
    'Healthcare systems worldwide struggle with timely and accurate',
    'disease identification. Delayed diagnosis increases patient risk',
    'and healthcare costs.',
    '',
    'GOAL: Build an AI model that classifies one of 10 disease',
    'conditions from patient vitals and symptoms using supervised',
    'machine learning with a Random Forest Classifier.',
    '',
    'Key Challenge: Multi-class classification with overlapping',
    'symptom patterns across 10 disease categories.',
])

# ── Disease Classes (right) ────────────────────────────────────────────────
card(margin * 2 + col_w, row1_y, col_w, 68)
section_header(margin * 2 + col_w, row1_y, col_w, '  DISEASE CLASSES (10 Categories)')

diseases = [
    '1. Flu              - Fever + Cough + Fatigue + High Temp',
    '2. Common Cold      - Cough + Runny Nose + Sore Throat',
    '3. Allergy          - Skin Rash + Runny Nose + Headache',
    '4. Migraine         - Headache + Fatigue (no fever)',
    '5. Food Poisoning   - Nausea + Vomiting + Fatigue',
    '6. Skin Infection   - Skin Rash + Fever',
    '7. Asthma           - Wheezing + Cough',
    '8. Hypertension Risk- High BP + Age > 40',
    '9. Diabetes Risk    - High Glucose + Age > 35',
    '10. Healthy         - No significant condition',
]
bullet(margin * 2 + col_w + 4, row1_y + 13, col_w - 8, diseases, size=9)

# ════════════════════════════════════════════════════════════════════════════
# ROW 2  (y=148)
# ════════════════════════════════════════════════════════════════════════════
row2_y = row1_y + 70
col3_w = (W - 4 * margin) / 3

# ── Dataset ───────────────────────────────────────────────────────────────────
card(margin, row2_y, col3_w, 72)
section_header(margin, row2_y, col3_w, '  DATASET')
feats = [
    'Records : 5,000 (synthetic)',
    'Features: 15 input variables',
    '',
    'Numeric:',
    '  age (5-84)',
    '  temperature_f (93.8-103F)',
    '  systolic_bp (95-184 mmHg)',
    '  glucose (70-239 mg/dL)',
    '',
    'Categorical:',
    '  sex (male / female)',
    '',
    'Binary Symptoms (0/1):',
    '  cough, fever, headache,',
    '  fatigue, runny_nose,',
    '  sore_throat, nausea,',
    '  vomiting, skin_rash,',
    '  wheezing',
]
body_text(margin + 4, row2_y + 12, col3_w - 8, feats, size=9)

# ── Methodology ───────────────────────────────────────────────────────────────
card(margin * 2 + col3_w, row2_y, col3_w, 72)
section_header(margin * 2 + col3_w, row2_y, col3_w, '  METHODOLOGY')
steps = [
    'Step 1: Dataset Generation',
    '  Rule-based synthetic data',
    '  for 10 disease classes (n=5000)',
    '',
    'Step 2: EDA',
    '  Distribution plots,',
    '  Correlation heatmap,',
    '  Class balance analysis',
    '',
    'Step 3: Preprocessing',
    '  One-Hot Encoding (sex)',
    '  80/20 Train-Test Split',
    '',
    'Step 4: Model Training',
    '  Random Forest Classifier',
    '  200 estimators, random_state=42',
    '',
    'Step 5: Deployment',
    '  Streamlit web application',
]
body_text(margin * 2 + col3_w + 4, row2_y + 12, col3_w - 8, steps, size=9)

# ── Model Results ─────────────────────────────────────────────────────────────
card(margin * 3 + col3_w * 2, row2_y, col3_w, 72)
section_header(margin * 3 + col3_w * 2, row2_y, col3_w, '  MODEL RESULTS', r=5, g=150, b=105)

# Result boxes
def metric_box(x, y, w, h, label, value, bg=(37, 99, 235)):
    pdf.set_fill_color(*bg)
    pdf.rect(x, y, w, h, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_xy(x, y + 2)
    pdf.cell(w, 9, safe(value), align='C')
    pdf.set_font('Helvetica', '', 8)
    pdf.set_xy(x, y + 11)
    pdf.cell(w, 5, safe(label), align='C')

bx = margin * 3 + col3_w * 2 + 6
metric_box(bx,       row2_y + 12, col3_w - 12, 18, 'Accuracy',  '~90%',  bg=(37, 99, 235))
metric_box(bx,       row2_y + 34, col3_w - 12, 18, 'Model',     'RF',    bg=(5, 150, 105))
metric_box(bx,       row2_y + 56, col3_w - 12, 14, 'Training Records', '4,000', bg=(124, 58, 237))

# ════════════════════════════════════════════════════════════════════════════
# ROW 3  (y=228)
# ════════════════════════════════════════════════════════════════════════════
row3_y = row2_y + 74

# ── Tech Stack ───────────────────────────────────────────────────────────────
card(margin, row3_y, col_w, 52)
section_header(margin, row3_y, col_w, '  TECH STACK')
tech = [
    'Python 3.11      - Core language',
    'pandas & NumPy   - Data manipulation',
    'scikit-learn     - ML pipeline & Random Forest',
    'matplotlib       - Visualisations',
    'seaborn          - Statistical plots',
    'Streamlit        - Interactive web application',
    'Jupyter Notebook - Analysis & reporting',
    'GitHub           - Version control & hosting',
]
bullet(margin + 4, row3_y + 12, col_w - 8, tech)

# ── Key Findings ──────────────────────────────────────────────────────────────
card(margin * 2 + col_w, row3_y, col_w, 52)
section_header(margin * 2 + col_w, row3_y, col_w, '  KEY FINDINGS')
findings = [
    'High-temperature + cough + fatigue strongly predicts Flu',
    'Wheezing is the dominant feature for Asthma detection',
    'Glucose > 200 at age > 35 reliably flags Diabetes Risk',
    'Systolic BP > 160 at age > 40 indicates Hypertension Risk',
    'Skin rash combined with fever differentiates Skin Infection',
    'Random Forest handles overlapping symptom patterns well',
    'Model achieves ~90% accuracy on unseen test data',
    'All 10 classes correctly predicted by the Streamlit app',
]
bullet(margin * 2 + col_w + 4, row3_y + 12, col_w - 8, findings)

# ════════════════════════════════════════════════════════════════════════════
# ROW 4  - ML Pipeline diagram + Live App
# ════════════════════════════════════════════════════════════════════════════
row4_y = row3_y + 54

# Pipeline visual
card(margin, row4_y, W - 2 * margin, 26, r=240, g=245, b=255)
section_header(margin, row4_y, W - 2 * margin, '  ML PIPELINE')

pipeline_steps = [
    ('Data\nGeneration', 37, 99, 235),
    ('EDA &\nVisualization', 5, 150, 105),
    ('Pre-\nprocessing', 124, 58, 237),
    ('Model\nTraining', 220, 38, 38),
    ('Evaluation', 234, 88, 12),
    ('Streamlit\nDeployment', 37, 99, 235),
]
step_w = (W - 2 * margin - 20) / len(pipeline_steps)
sx = margin + 10
sy = row4_y + 11

for i, (label, r, g, b) in enumerate(pipeline_steps):
    pdf.set_fill_color(r, g, b)
    pdf.rect(sx + i * step_w, sy, step_w - 6, 13, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_xy(sx + i * step_w, sy + 3)
    pdf.cell(step_w - 6, 7, safe(label.replace('\n', ' ')), align='C')
    if i < len(pipeline_steps) - 1:
        pdf.set_text_color(37, 99, 235)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_xy(sx + i * step_w + step_w - 7, sy + 3)
        pdf.cell(7, 7, '->', align='C')

# ── Live App banner ────────────────────────────────────────────────────────────
row5_y = row4_y + 28
pdf.set_fill_color(5, 150, 105)
pdf.rect(margin, row5_y, W - 2 * margin, 16, 'F')
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_xy(margin, row5_y + 2)
pdf.cell(W - 2 * margin, 6, safe('LIVE STREAMLIT APPLICATION'), align='C')
pdf.set_font('Helvetica', '', 9)
pdf.set_xy(margin, row5_y + 8)
pdf.cell(W - 2 * margin, 6,
         safe('https://1roahan3-droiroahn-ai-multi-disease-prediction-app-wpqa56.streamlit.app/'),
         align='C')

# ── GitHub ─────────────────────────────────────────────────────────────────────
row6_y = row5_y + 18
pdf.set_fill_color(15, 52, 96)
pdf.rect(margin, row6_y, W - 2 * margin, 14, 'F')
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica', 'B', 10)
pdf.set_xy(margin, row6_y + 2)
pdf.cell(W - 2 * margin, 5, safe('GitHub Repository'), align='C')
pdf.set_font('Helvetica', '', 9)
pdf.set_xy(margin, row6_y + 7)
pdf.cell(W - 2 * margin, 5,
         safe('https://github.com/1roahan3-droiroahn/ai_multi_disease_prediction'),
         align='C')

# ── Footer ─────────────────────────────────────────────────────────────────────
pdf.set_fill_color(15, 52, 96)
pdf.rect(0, H - 14, W, 14, 'F')
pdf.set_text_color(180, 200, 255)
pdf.set_font('Helvetica', '', 9)
pdf.set_xy(0, H - 10)
pdf.cell(W, 6,
         safe('Pancholi Rohankumar Ashvinbhai | Enrollment: 251370680011 | GTU PGDDS Mini Project 2025-26'),
         align='C')

pdf.output(OUTPUT)
print(f"Poster saved: {OUTPUT}")
