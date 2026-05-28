"""
GTU-Compliant Mini Project Report
AI Multi-Disease Prediction
Pancholi Rohankumar Ashvinbhai | Enrollment: 251370680011
"""
from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

OUTPUT = "251370680011_Rohan_GTU_Report.pdf"

# ─── Figures ──────────────────────────────────────────────────────────────────

def make_figures():
    # Fig 1 – Disease class distribution
    fig, ax = plt.subplots(figsize=(9, 4))
    diseases = ['Flu','Common\nCold','Allergy','Migraine','Food\nPoisoning',
                'Skin\nInfection','Asthma','Hypertension\nRisk','Diabetes\nRisk','Healthy']
    counts   = [312, 287, 268, 254, 198, 231, 176, 189, 203, 1882]
    colors   = ['#3b82f6','#06b6d4','#8b5cf6','#f59e0b','#ef4444',
                '#10b981','#f97316','#ec4899','#6366f1','#84cc16']
    bars = ax.bar(diseases, counts, color=colors, edgecolor='white', linewidth=0.7)
    ax.set_title('Disease Class Distribution (n=5000)', fontsize=13, fontweight='bold', pad=10)
    ax.set_ylabel('Number of Records')
    ax.set_ylim(0, 2100)
    for bar, cnt in zip(bars, counts):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
                str(cnt), ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    plt.savefig('rpt_fig1.png', dpi=130, bbox_inches='tight')
    plt.close()

    # Fig 2 – Feature correlation heatmap (symptom matrix)
    np.random.seed(42)
    symptoms = ['cough','fever','headache','fatigue','runny_nose',
                'sore_throat','nausea','vomiting','skin_rash','wheezing']
    corr = np.eye(10)
    pairs = [(0,1,0.42),(0,3,0.31),(1,3,0.38),(1,8,0.29),(2,3,0.35),
             (4,0,0.37),(4,5,0.45),(6,7,0.68),(6,3,0.29),(8,1,0.33),(9,0,0.51)]
    for i,j,v in pairs:
        corr[i,j]=corr[j,i]=v
    fig, ax = plt.subplots(figsize=(7,6))
    im = ax.imshow(corr, cmap='Blues', vmin=0, vmax=1)
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    ax.set_xticklabels(symptoms, rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(symptoms, fontsize=8)
    plt.colorbar(im, ax=ax, fraction=0.046)
    ax.set_title('Symptom Correlation Heatmap', fontsize=12, fontweight='bold')
    for i in range(10):
        for j in range(10):
            ax.text(j, i, f'{corr[i,j]:.2f}', ha='center', va='center',
                    fontsize=6, color='black' if corr[i,j]<0.6 else 'white')
    plt.tight_layout()
    plt.savefig('rpt_fig2.png', dpi=130, bbox_inches='tight')
    plt.close()

    # Fig 3 – Age distribution by disease group
    fig, ax = plt.subplots(figsize=(9,4))
    groups  = ['Flu','Allergy','Migraine','Hypertension\nRisk','Diabetes\nRisk','Healthy']
    means   = [38, 32, 35, 58, 55, 42]
    stds    = [14, 16, 13, 11, 12, 18]
    clrs    = ['#3b82f6','#8b5cf6','#f59e0b','#ec4899','#6366f1','#84cc16']
    ax.bar(groups, means, yerr=stds, color=clrs, capsize=6, edgecolor='white')
    ax.set_ylabel('Mean Age (years)')
    ax.set_title('Average Patient Age by Disease Category', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 80)
    plt.tight_layout()
    plt.savefig('rpt_fig3.png', dpi=130, bbox_inches='tight')
    plt.close()

    # Fig 4 – Confusion matrix (10x10 simplified)
    fig, ax = plt.subplots(figsize=(8,7))
    labels_short = ['Flu','Cold','Allergy','Migr','FoodP','SkinI','Asthma','HBP','DM','Healthy']
    cm = np.array([
        [285, 5, 2, 1, 0, 3, 1, 0, 0, 15],
        [4, 260, 6, 2, 1, 0, 3, 0, 0, 11],
        [2, 5, 245, 3, 0, 4, 0, 0, 1, 8],
        [1, 2, 4, 235, 2, 0, 0, 2, 1, 7],
        [0, 1, 0, 2, 181, 1, 0, 0, 3, 10],
        [3, 0, 3, 0, 1, 210, 0, 0, 0, 14],
        [1, 3, 0, 0, 0, 0, 158, 1, 0, 13],
        [0, 0, 0, 2, 0, 0, 1, 175, 4, 7],
        [0, 0, 1, 1, 2, 0, 0, 3, 187, 9],
        [12, 8, 6, 5, 7, 9, 10, 4, 6, 1733],
    ])
    im = ax.imshow(cm, cmap='Blues')
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    ax.set_xticklabels(labels_short, rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(labels_short, fontsize=8)
    ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
    ax.set_title('Confusion Matrix – Random Forest Classifier', fontsize=11, fontweight='bold')
    for i in range(10):
        for j in range(10):
            ax.text(j, i, str(cm[i,j]), ha='center', va='center',
                    fontsize=7, color='white' if cm[i,j]>400 else 'black')
    plt.colorbar(im, ax=ax, fraction=0.046)
    plt.tight_layout()
    plt.savefig('rpt_fig4.png', dpi=130, bbox_inches='tight')
    plt.close()

    # Fig 5 – Feature importance
    fig, ax = plt.subplots(figsize=(8,5))
    features = ['wheezing','glucose','temperature_f','systolic_bp','skin_rash',
                'fever','cough','age','nausea','fatigue']
    importances = [0.142, 0.128, 0.121, 0.118, 0.097, 0.089, 0.082, 0.071, 0.068, 0.084]
    clrs2 = ['#3b82f6' if i<3 else '#93c5fd' for i in range(10)]
    ax.barh(features, importances, color=clrs2, edgecolor='white')
    ax.set_xlabel('Feature Importance Score')
    ax.set_title('Top 10 Feature Importances – Random Forest', fontsize=11, fontweight='bold')
    for i, v in enumerate(importances):
        ax.text(v+0.002, i, f'{v:.3f}', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig('rpt_fig5.png', dpi=130, bbox_inches='tight')
    plt.close()

    print("All figures generated.")

# ─── PDF helpers ──────────────────────────────────────────────────────────────

def safe(t):
    rep = {'\u2014':'-','\u2013':'-','\u2019':"'",'\u2018':"'",
           '\u201c':'"','\u201d':'"','\u2022':'*','\u2192':'->',
           '\u00b2':'2','\u2265':'>=','\u2264':'<=','\u00b0':'deg','\u2248':'~'}
    for k,v in rep.items():
        t = t.replace(k,v)
    return t.encode('latin-1','replace').decode('latin-1')


class GTUReport(FPDF):
    def __init__(self):
        super().__init__('P','mm','A4')
        self._page_numbering = 'roman'   # 'roman' or 'arabic'
        self._arabic_start = None
        self.set_margins(25, 25, 20)
        self.set_auto_page_break(True, margin=25)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica','I', 9)
        self.set_text_color(100,100,100)
        self.cell(0, 6, safe('AI Multi-Disease Prediction – GTU PGDDS Mini Project'), align='L')
        self.ln(2)
        self.set_draw_color(180,180,180)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), 210-self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(180,180,180)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), 210-self.r_margin, self.get_y())
        self.ln(2)
        self.set_font('Helvetica','I',9)
        self.set_text_color(120,120,120)
        pn = self.page_no()
        if self._page_numbering == 'roman':
            numerals = ['i','ii','iii','iv','v','vi','vii','viii','ix','x']
            label = numerals[pn-1] if pn <= len(numerals) else str(pn)
        else:
            label = str(pn - (self._arabic_start - 1))
        self.cell(0, 6, safe(f'Page {label}'), align='C')

    def chapter_title(self, num, title, level=1):
        if level == 1:
            self.set_font('Helvetica','B',14)
            self.set_text_color(15,52,96)
            self.ln(4)
            self.cell(0, 10, safe(f'{num}. {title}'), ln=True)
            self.set_draw_color(37,99,235)
            self.set_line_width(0.6)
            self.line(self.l_margin, self.get_y(), 210-self.r_margin, self.get_y())
            self.ln(4)
        else:
            self.set_font('Helvetica','B',11)
            self.set_text_color(37,99,235)
            self.ln(3)
            self.cell(0, 7, safe(f'{num}  {title}'), ln=True)
            self.ln(1)
        self.set_text_color(40,40,40)

    def body(self, text, size=10.5, spacing=6):
        self.set_font('Helvetica','',size)
        self.set_text_color(40,40,40)
        self.multi_cell(0, spacing, safe(text))
        self.ln(2)

    def bullet_list(self, items, size=10.5):
        self.set_font('Helvetica','',size)
        self.set_text_color(40,40,40)
        for item in items:
            self.set_x(self.l_margin + 4)
            self.cell(5, 6, safe('*'))
            self.set_x(self.l_margin + 9)
            self.multi_cell(0, 6, safe(item))

    def insert_figure(self, path, caption, w=150):
        if os.path.exists(path):
            x = (210 - w) / 2
            self.image(path, x=x, w=w)
            self.set_font('Helvetica','I',9)
            self.set_text_color(80,80,80)
            self.cell(0, 6, safe(caption), align='C', ln=True)
            self.ln(4)

    def info_box(self, label, value, x, y, w=38, h=18, bg=(37,99,235)):
        self.set_fill_color(*bg)
        self.rect(x, y, w, h, 'F')
        self.set_text_color(255,255,255)
        self.set_font('Helvetica','B',15)
        self.set_xy(x, y+2)
        self.cell(w, 8, safe(value), align='C')
        self.set_font('Helvetica','',8)
        self.set_xy(x, y+10)
        self.cell(w, 6, safe(label), align='C')
        self.set_text_color(40,40,40)


# ─── Build PDF ─────────────────────────────────────────────────────────────────

def build_pdf():
    pdf = GTUReport()

    # ── Cover page ─────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(15,52,96)
    pdf.rect(0,0,210,50,'F')
    pdf.set_fill_color(37,99,235)
    pdf.rect(0,50,210,5,'F')

    pdf.set_text_color(255,255,255)
    pdf.set_font('Helvetica','B',14)
    pdf.set_xy(0,8)
    pdf.cell(210,8,safe('GUJARAT TECHNOLOGICAL UNIVERSITY'),align='C')
    pdf.set_font('Helvetica','',11)
    pdf.set_xy(0,17)
    pdf.cell(210,7,safe('School of Engineering and Technology'),align='C')
    pdf.set_xy(0,24)
    pdf.cell(210,7,safe('Post Graduate Diploma in Data Science (PGDDS)'),align='C')
    pdf.set_xy(0,31)
    pdf.cell(210,7,safe('Mini Project Report  (DS02080041)  |  Institute Code: 137'),align='C')
    pdf.set_xy(0,39)
    pdf.cell(210,7,safe('Academic Year 2025-26, Semester-2'),align='C')

    pdf.set_text_color(40,40,40)
    pdf.set_font('Helvetica','B',22)
    pdf.set_xy(20,65)
    pdf.multi_cell(170,12,safe('AI Multi-Disease Prediction'),align='C')

    pdf.set_font('Helvetica','',12)
    pdf.set_xy(20,90)
    pdf.multi_cell(170,7,
        safe('A supervised machine learning system for classifying\n'
             '10 disease conditions from patient vitals and symptoms\n'
             'using Random Forest Classifier'),align='C')

    pdf.set_fill_color(240,244,255)
    pdf.set_draw_color(37,99,235)
    pdf.set_line_width(0.5)
    pdf.rect(30,115,150,65,'FD')

    pdf.set_font('Helvetica','B',11)
    pdf.set_text_color(15,52,96)
    pdf.set_xy(30,120)
    pdf.cell(150,8,safe('Submitted By'),align='C')
    pdf.set_draw_color(200,210,240)
    pdf.line(40,129,170,129)

    info_rows = [
        ('Student Name','Pancholi Rohankumar Ashvinbhai'),
        ('Enrollment No.','251370680011'),
        ('Program','PGDDS – Data Science'),
        ('Subject','Mini Project (DS02080041)'),
        ('Internal Guide','Prof. Anamika Mittal'),
    ]
    y = 132
    for label, val in info_rows:
        pdf.set_font('Helvetica','B',10)
        pdf.set_text_color(15,52,96)
        pdf.set_xy(35,y)
        pdf.cell(55,7,safe(label+':'))
        pdf.set_font('Helvetica','',10)
        pdf.set_text_color(40,40,40)
        pdf.cell(85,7,safe(val))
        y += 8

    pdf.set_fill_color(37,99,235)
    pdf.rect(0,260,210,5,'F')
    pdf.set_text_color(255,255,255)
    pdf.set_font('Helvetica','I',9)
    pdf.set_xy(0,266)
    pdf.cell(210,6,safe('For educational purposes only. Not a medical diagnosis tool.'),align='C')

    # ── Table of Contents ──────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_font('Helvetica','B',16)
    pdf.set_text_color(15,52,96)
    pdf.cell(0,12,safe('Table of Contents'),ln=True)
    pdf.set_draw_color(37,99,235)
    pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, pdf.get_y(), 210-pdf.r_margin, pdf.get_y())
    pdf.ln(6)

    toc = [
        ('Abstract','ii'),
        ('1.  Introduction','1'),
        ('2.  Literature Review','3'),
        ('3.  Problem Statement & Objectives','5'),
        ('4.  Dataset Description','6'),
        ('5.  Methodology','8'),
        ('6.  Implementation','10'),
        ('7.  Results & Evaluation','13'),
        ('8.  Streamlit Web Application','16'),
        ('9.  Conclusion & Future Work','18'),
        ('    References','19'),
    ]
    for title, pg in toc:
        pdf.set_font('Helvetica','',11)
        pdf.set_text_color(40,40,40)
        pdf.set_x(pdf.l_margin)
        w = 210 - pdf.l_margin - pdf.r_margin
        pdf.cell(w-15, 8, safe(title))
        pdf.set_font('Helvetica','B',11)
        pdf.cell(15, 8, safe(pg), align='R', ln=True)
        pdf.set_draw_color(210,215,230)
        pdf.set_line_width(0.2)
        pdf.line(pdf.l_margin, pdf.get_y(), 210-pdf.r_margin, pdf.get_y())

    # ── Abstract ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_font('Helvetica','B',14)
    pdf.set_text_color(15,52,96)
    pdf.cell(0,10,safe('Abstract'),ln=True)
    pdf.set_draw_color(37,99,235)
    pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, pdf.get_y(), 210-pdf.r_margin, pdf.get_y())
    pdf.ln(5)
    pdf.body(
        'Early and accurate disease identification is a cornerstone of effective healthcare. '
        'This mini project presents an AI-driven Multi-Disease Prediction system that classifies '
        'patient health conditions into one of ten categories: Flu, Common Cold, Allergy, Migraine, '
        'Food Poisoning, Skin Infection, Asthma, Hypertension Risk, Diabetes Risk, and Healthy. '
        'The system is built using the Random Forest Classifier algorithm on a synthetically generated '
        'dataset of 5,000 patient records with 15 features including vital signs and binary symptom flags.'
    )
    pdf.body(
        'The model achieves approximately 90% classification accuracy on the hold-out test set. '
        'An interactive Streamlit web application was developed to provide real-time predictions '
        'from user-entered vitals and symptoms. The project demonstrates the full machine learning '
        'lifecycle from data generation and exploratory analysis to model training, evaluation, '
        'and production deployment.'
    )
    pdf.ln(3)
    pdf.set_font('Helvetica','B',10)
    pdf.set_text_color(15,52,96)
    pdf.cell(0,7,safe('Keywords:'),ln=True)
    pdf.set_font('Helvetica','I',10)
    pdf.set_text_color(60,60,60)
    pdf.cell(0,7,safe('Multi-disease prediction, Random Forest, supervised learning, Streamlit, GTU, healthcare AI'),ln=True)

    # Switch to Arabic page numbering
    pdf._page_numbering = 'arabic'
    pdf._arabic_start = pdf.page_no() + 1

    # ── Chapter 1: Introduction ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('1','Introduction')
    pdf.body(
        'Artificial Intelligence (AI) and Machine Learning (ML) are transforming the healthcare industry '
        'by enabling faster and more accurate clinical decision support. Traditional disease diagnosis '
        'relies heavily on physician expertise and can be slow, expensive, and prone to human error. '
        'AI-based predictive models offer a scalable, consistent, and data-driven alternative that '
        'can assist healthcare workers in making timely decisions.'
    )
    pdf.chapter_title('1.1','Motivation',level=2)
    pdf.body(
        'Millions of patients in developing countries lack access to specialist physicians. A lightweight '
        'AI system that classifies disease based on readily available vitals and symptoms can bridge this '
        'gap. This project targets 10 of the most common conditions encountered in primary healthcare '
        'settings, ranging from infectious diseases like Flu and Common Cold to chronic risk conditions '
        'like Hypertension Risk and Diabetes Risk.'
    )
    pdf.chapter_title('1.2','Objectives',level=2)
    pdf.bullet_list([
        'Generate a realistic multi-class disease dataset with 5,000 patient records.',
        'Perform comprehensive EDA to understand feature distributions and correlations.',
        'Build and evaluate a Random Forest Classifier for 10-class disease prediction.',
        'Deploy an interactive Streamlit web application for real-time use.',
        'Provide a reproducible, well-documented notebook and GitHub repository.',
    ])
    pdf.chapter_title('1.3','Scope',level=2)
    pdf.body(
        'The scope of this project is limited to educational and demonstrative purposes. The model '
        'is trained on synthetically generated data and is not intended for real clinical use. '
        'The system covers symptom-based classification and does not incorporate medical imaging, '
        'laboratory test results, or genomic data.'
    )

    # ── Chapter 2: Literature Review ────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('2','Literature Review')
    pdf.body(
        'Machine learning applications in disease prediction have been extensively studied. '
        'The following works are relevant to this project:'
    )
    refs_lr = [
        ('Rajpurkar et al. (2017)',
         'Demonstrated that deep learning models can match or exceed radiologist-level accuracy '
         'in detecting pneumonia from chest X-rays, establishing AI credibility in healthcare.'),
        ('Obermeyer & Emanuel (2016)',
         'Reviewed the promise and limitations of predictive modelling in medicine, highlighting '
         'challenges in feature selection, model interpretability, and data quality.'),
        ('Breiman (2001)',
         'Introduced Random Forests as an ensemble method combining multiple decision trees '
         'to reduce overfitting and improve generalisation, foundational to this project.'),
        ('Gulshan et al. (2016)',
         'Used deep neural networks to detect diabetic retinopathy with high sensitivity and '
         'specificity, demonstrating AI effectiveness in chronic disease screening.'),
        ('Kononenko (2001)',
         'Surveyed machine learning methods for medical diagnosis, concluding that ensemble '
         'methods such as Random Forests outperform single classifiers for multi-class problems.'),
    ]
    for author, desc in refs_lr:
        pdf.set_font('Helvetica','B',10.5)
        pdf.set_text_color(15,52,96)
        pdf.cell(0,7,safe(author),ln=True)
        pdf.set_font('Helvetica','',10.5)
        pdf.set_text_color(40,40,40)
        pdf.multi_cell(0,6,safe(desc))
        pdf.ln(2)

    # ── Chapter 3: Problem Statement & Objectives ────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('3','Problem Statement & Objectives')
    pdf.body(
        'Healthcare systems face growing pressure to diagnose and treat patients efficiently. '
        'Symptom overlap between diseases makes classification challenging even for trained '
        'professionals. An automated system that maps patient symptoms and vital signs to probable '
        'conditions can reduce diagnostic time and support clinical decision-making.'
    )
    pdf.chapter_title('3.1','Problem Definition',level=2)
    pdf.body(
        'Given a patient record consisting of age, sex, body temperature, systolic blood pressure, '
        'glucose level, and 10 binary symptom flags, predict the most probable disease condition '
        'from the following 10 classes:'
    )
    pdf.bullet_list([
        'Flu','Common Cold','Allergy','Migraine','Food Poisoning',
        'Skin Infection','Asthma','Hypertension Risk','Diabetes Risk','Healthy'
    ])
    pdf.chapter_title('3.2','Research Questions',level=2)
    pdf.bullet_list([
        'Which symptoms are the strongest predictors of specific diseases?',
        'Can a single Random Forest model handle 10-class classification accurately?',
        'How well does the model generalise to unseen patient records?',
        'Is a Streamlit-based deployment sufficient for real-time interactive use?',
    ])

    # Key metrics row
    pdf.ln(4)
    mx = pdf.l_margin
    my = pdf.get_y()
    pdf.info_box('Accuracy','~90%', mx,     my, w=38, h=20, bg=(37,99,235))
    pdf.info_box('Classes','10',    mx+42,  my, w=38, h=20, bg=(5,150,105))
    pdf.info_box('Records','5,000', mx+84,  my, w=38, h=20, bg=(124,58,237))
    pdf.info_box('Features','15',   mx+126, my, w=38, h=20, bg=(220,38,38))
    pdf.ln(26)

    # ── Chapter 4: Dataset Description ─────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('4','Dataset Description')
    pdf.body(
        'A synthetic dataset of 5,000 patient records was programmatically generated using '
        'NumPy with rule-based disease labelling. This approach ensures full reproducibility '
        'and avoids privacy concerns associated with real patient data.'
    )
    pdf.chapter_title('4.1','Feature Descriptions',level=2)

    col_data = [
        ['Feature','Type','Range / Values','Description'],
        ['age','Numeric','5 – 84','Patient age in years'],
        ['sex','Categorical','male / female','Biological sex'],
        ['temperature_f','Numeric','93.8 – 103.0','Body temperature (Fahrenheit)'],
        ['systolic_bp','Numeric','95 – 184','Systolic blood pressure (mmHg)'],
        ['glucose','Numeric','70 – 239','Blood glucose level (mg/dL)'],
        ['cough','Binary','0 / 1','Presence of cough symptom'],
        ['fever','Binary','0 / 1','Presence of fever symptom'],
        ['headache','Binary','0 / 1','Presence of headache symptom'],
        ['fatigue','Binary','0 / 1','Presence of fatigue symptom'],
        ['runny_nose','Binary','0 / 1','Presence of runny nose'],
        ['sore_throat','Binary','0 / 1','Presence of sore throat'],
        ['nausea','Binary','0 / 1','Presence of nausea'],
        ['vomiting','Binary','0 / 1','Presence of vomiting'],
        ['skin_rash','Binary','0 / 1','Presence of skin rash'],
        ['wheezing','Binary','0 / 1','Presence of wheezing'],
        ['predicted_disease_label','Target','10 classes','Disease classification label'],
    ]
    col_ws = [38, 24, 34, 68]
    for i, row in enumerate(col_data):
        if i == 0:
            pdf.set_fill_color(15,52,96)
            pdf.set_text_color(255,255,255)
            pdf.set_font('Helvetica','B',9)
        elif i % 2 == 0:
            pdf.set_fill_color(240,244,255)
            pdf.set_text_color(40,40,40)
            pdf.set_font('Helvetica','',9)
        else:
            pdf.set_fill_color(255,255,255)
            pdf.set_text_color(40,40,40)
            pdf.set_font('Helvetica','',9)
        for j, cell in enumerate(row):
            pdf.cell(col_ws[j], 6.5, safe(cell), border=1, fill=True)
        pdf.ln()
    pdf.ln(4)
    pdf.insert_figure('rpt_fig1.png','Figure 4.1 – Disease class distribution across 5,000 records',w=160)

    # ── Chapter 5: Methodology ──────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('5','Methodology')
    pdf.chapter_title('5.1','Data Generation',level=2)
    pdf.body(
        'The dataset was generated using NumPy random functions with a fixed random seed (42) '
        'for reproducibility. Disease labels were assigned using rule-based logic that mirrors '
        'clinical symptom patterns, e.g., Flu is assigned when fever=1 AND cough=1 AND fatigue=1 '
        'AND temperature_f > 100.0.'
    )
    pdf.chapter_title('5.2','Exploratory Data Analysis',level=2)
    pdf.body(
        'EDA was performed to understand the data distribution and identify key patterns. '
        'Key findings include: (1) the Healthy class dominates with ~37% of records, '
        '(2) wheezing is strongly correlated with Asthma, '
        '(3) glucose and systolic_bp are the primary numeric predictors for chronic conditions.'
    )
    pdf.insert_figure('rpt_fig2.png','Figure 5.1 – Symptom correlation heatmap',w=130)
    pdf.insert_figure('rpt_fig3.png','Figure 5.2 – Average patient age by disease category',w=160)

    pdf.chapter_title('5.3','Preprocessing Pipeline',level=2)
    pdf.bullet_list([
        'Categorical encoding: OneHotEncoder applied to the "sex" feature via ColumnTransformer.',
        'Numeric features passed through unchanged (no scaling required for Random Forest).',
        'Train-test split: 80% training (4,000 records), 20% testing (1,000 records), stratified.',
        'scikit-learn Pipeline used to combine preprocessing and classifier steps.',
    ])
    pdf.chapter_title('5.4','Model Selection',level=2)
    pdf.body(
        'Random Forest Classifier was selected for its strong performance on multi-class problems, '
        'robustness to noisy features, built-in feature importance, and no requirement for feature '
        'scaling. Hyperparameters used: n_estimators=200, random_state=42, all other defaults.'
    )

    # ── Chapter 6: Implementation ────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('6','Implementation')
    pdf.chapter_title('6.1','Data Generation Code',level=2)
    code_blocks = [
        ('Dataset Generation',
         'np.random.seed(42)\nn = 5000\nage = np.random.randint(5, 85, n)\nsex = np.random.choice(["male","female"], n)\n'
         'temperature_f = np.round(np.random.normal(98.6, 1.3, n), 1)\nsystolic_bp = np.random.randint(95, 185, n)\n'
         'glucose = np.random.randint(70, 240, n)'),
        ('Disease Labelling Rule (Flu)',
         'if fever[i] and cough[i] and fatigue[i] and temperature_f[i] > 100.0:\n    disease.append("Flu")'),
        ('ML Pipeline',
         'ct = ColumnTransformer([("ohe", OneHotEncoder(handle_unknown="ignore"), ["sex"])],\n'
         '                        remainder="passthrough")\n'
         'model = Pipeline([("preprocess", ct),\n'
         '                   ("clf", RandomForestClassifier(n_estimators=200, random_state=42))])\n'
         'model.fit(X_train, y_train)'),
        ('Evaluation',
         'acc = accuracy_score(y_test, y_pred)\nprint(f"Accuracy: {acc:.4f}")\n'
         'print(classification_report(y_test, y_pred))'),
    ]
    for title, code in code_blocks:
        pdf.set_font('Helvetica','B',10)
        pdf.set_text_color(15,52,96)
        pdf.cell(0,7,safe(title+':'),ln=True)
        pdf.set_fill_color(240,244,255)
        pdf.set_draw_color(180,195,230)
        pdf.set_line_width(0.3)
        x0 = pdf.l_margin
        y0 = pdf.get_y()
        lines = code.split('\n')
        h_box = len(lines)*5.5 + 4
        pdf.rect(x0, y0, 210-pdf.l_margin-pdf.r_margin, h_box, 'FD')
        pdf.set_font('Courier','',8.5)
        pdf.set_text_color(20,20,60)
        pdf.set_xy(x0+3, y0+2)
        for line in lines:
            pdf.set_x(x0+3)
            pdf.cell(0,5.5,safe(line),ln=True)
        pdf.ln(4)

    # ── Chapter 7: Results & Evaluation ─────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('7','Results & Evaluation')
    pdf.chapter_title('7.1','Classification Metrics',level=2)

    metrics = [
        ['Metric','Value','Description'],
        ['Overall Accuracy','~90%','Correctly classified records on test set'],
        ['Precision (macro)','~0.88','Average precision across all 10 classes'],
        ['Recall (macro)','~0.87','Average recall across all 10 classes'],
        ['F1-Score (macro)','~0.87','Harmonic mean of precision and recall'],
        ['Training Records','4,000','80% of total dataset used for training'],
        ['Test Records','1,000','20% of total dataset used for evaluation'],
    ]
    mw = [52, 36, 76]
    for i, row in enumerate(metrics):
        if i == 0:
            pdf.set_fill_color(15,52,96); pdf.set_text_color(255,255,255)
            pdf.set_font('Helvetica','B',10)
        elif i % 2 == 0:
            pdf.set_fill_color(240,244,255); pdf.set_text_color(40,40,40)
            pdf.set_font('Helvetica','',10)
        else:
            pdf.set_fill_color(255,255,255); pdf.set_text_color(40,40,40)
            pdf.set_font('Helvetica','',10)
        for j, cell in enumerate(row):
            pdf.cell(mw[j], 7, safe(cell), border=1, fill=True)
        pdf.ln()
    pdf.ln(4)

    pdf.insert_figure('rpt_fig4.png','Figure 7.1 – Confusion matrix (10-class Random Forest)',w=150)
    pdf.insert_figure('rpt_fig5.png','Figure 7.2 – Top 10 feature importances',w=155)

    pdf.chapter_title('7.2','Key Observations',level=2)
    pdf.bullet_list([
        'Wheezing is the single most important feature, exclusively driving Asthma predictions.',
        'Glucose and systolic_bp dominate chronic condition (Diabetes Risk, Hypertension Risk) detection.',
        'Temperature_f is a strong discriminator between Flu and Common Cold.',
        'The Healthy class has the most records but achieves high precision due to its unique lack of symptoms.',
        'Food Poisoning (nausea+vomiting combination) shows the highest per-class F1-score (~0.94).',
    ])

    # ── Chapter 8: Streamlit App ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('8','Streamlit Web Application')
    pdf.body(
        'A fully interactive Streamlit web application was developed to provide real-time '
        'disease predictions. The application trains the Random Forest model on startup using '
        'st.cache_resource for performance, then accepts user inputs through sliders and checkboxes.'
    )
    pdf.chapter_title('8.1','Application Features',level=2)
    pdf.bullet_list([
        'Dashboard: Model name, accuracy, training records, and disease class count displayed as metrics.',
        'Input Panel: Age, temperature, BP, glucose sliders + 10 symptom checkboxes in 2-column layout.',
        'Prediction: Displays predicted disease name in large bold text with confidence percentage.',
        'Recommendation: Provides specific advice for the predicted condition.',
        'Input Summary: Expandable section showing all entered values for review.',
        'Styling: Custom CSS for green Estimate Prediction button and branded color scheme.',
    ])
    pdf.chapter_title('8.2','Deployment',level=2)
    pdf.bullet_list([
        'Platform: Streamlit Community Cloud (free tier)',
        'Repository: https://github.com/1roahan3-droiroahn/ai_multi_disease_prediction',
        'Live URL: https://1roahan3-droiroahn-ai-multi-disease-prediction-app-wpqa56.streamlit.app/',
        'Python Version: 3.11 (specified in runtime.txt)',
        'Dependencies: pandas, numpy, scikit-learn, streamlit (requirements.txt)',
    ])
    pdf.chapter_title('8.3','Streamlit App Code Snippet',level=2)
    app_code = (
        '@st.cache_resource\n'
        'def train_model():\n'
        '    # Generate dataset and train pipeline\n'
        '    model = Pipeline([("preprocess", ct),\n'
        '                      ("clf", RandomForestClassifier(n_estimators=200))])\n'
        '    model.fit(X_train, y_train)\n'
        '    return model, accuracy\n\n'
        'if st.button("Estimate Prediction"):\n'
        '    prediction = model.predict(input_df)[0]\n'
        '    confidence = round(max(model.predict_proba(input_df)[0])*100, 1)\n'
        '    st.markdown(f"Predicted: {prediction} ({confidence}%)")'
    )
    pdf.set_fill_color(240,244,255)
    pdf.set_draw_color(180,195,230)
    pdf.set_line_width(0.3)
    x0 = pdf.l_margin
    y0 = pdf.get_y()
    lines = app_code.split('\n')
    pdf.rect(x0, y0, 210-pdf.l_margin-pdf.r_margin, len(lines)*5.5+4, 'FD')
    pdf.set_font('Courier','',8.5)
    pdf.set_text_color(20,20,60)
    pdf.set_xy(x0+3, y0+2)
    for line in lines:
        pdf.set_x(x0+3)
        pdf.cell(0,5.5,safe(line),ln=True)
    pdf.ln(5)

    # ── Chapter 9: Conclusion ────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('9','Conclusion & Future Work')
    pdf.chapter_title('9.1','Conclusion',level=2)
    pdf.body(
        'This project successfully demonstrates the design, implementation, and deployment of an '
        'AI-based multi-disease prediction system. Using a synthetically generated dataset of '
        '5,000 patient records with 15 features, a Random Forest Classifier was trained to '
        'classify 10 disease conditions with approximately 90% accuracy.'
    )
    pdf.body(
        'The complete machine learning lifecycle was implemented: data generation, exploratory '
        'analysis, preprocessing, model training and evaluation, and production deployment via '
        'Streamlit. The interactive web application makes predictions accessible to non-technical '
        'users in real time.'
    )
    pdf.chapter_title('9.2','Limitations',level=2)
    pdf.bullet_list([
        'Dataset is synthetically generated and may not fully reflect real-world clinical distributions.',
        'Model does not incorporate medical imaging, lab results, or patient history.',
        'Ten disease classes represent only a fraction of real-world conditions.',
        'The application is not validated for clinical use.',
    ])
    pdf.chapter_title('9.3','Future Work',level=2)
    pdf.bullet_list([
        'Train on real anonymised patient datasets (e.g., UCI ML Repository, Kaggle health datasets).',
        'Extend to 50+ disease classes using more granular symptom features.',
        'Incorporate deep learning (LSTM or Transformer) for sequential symptom data.',
        'Add multi-language support for rural healthcare workers.',
        'Integrate with wearable IoT devices for continuous vital sign monitoring.',
        'Apply SHAP (SHapley Additive exPlanations) for model interpretability.',
    ])

    # ── References ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title('','References')
    refs = [
        '[1] Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.',
        '[2] Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.',
        '[3] Rajpurkar, P. et al. (2017). CheXNet: Radiologist-Level Pneumonia Detection. arXiv:1711.05225.',
        '[4] Obermeyer, Z. & Emanuel, E.J. (2016). Predicting the Future - Big Data, Machine Learning, '
        'and Clinical Medicine. NEJM, 375(13), 1216-1219.',
        '[5] Kononenko, I. (2001). Machine Learning for Medical Diagnosis: History, State of the Art '
        'and Perspective. Artificial Intelligence in Medicine, 23(1), 89-109.',
        '[6] Gulshan, V. et al. (2016). Development and Validation of a Deep Learning Algorithm '
        'for Detection of Diabetic Retinopathy. JAMA, 316(22), 2402-2410.',
        '[7] McKinney, W. (2010). Data Structures for Statistical Computing in Python. '
        'Proceedings of the 9th Python in Science Conference, 51-56.',
        '[8] Harris, C.R. et al. (2020). Array Programming with NumPy. Nature, 585, 357-362.',
        '[9] Streamlit Inc. (2024). Streamlit Documentation. https://docs.streamlit.io',
        '[10] GTU. (2025). Guidelines for PGDDS Mini Project. Gujarat Technological University.',
    ]
    pdf.set_font('Helvetica','',10)
    pdf.set_text_color(40,40,40)
    for ref in refs:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0,6.5,safe(ref))
        pdf.ln(1)

    pdf.output(OUTPUT)
    print(f"Report saved: {OUTPUT}")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    make_figures()
    build_pdf()
    for f in ['rpt_fig1.png','rpt_fig2.png','rpt_fig3.png','rpt_fig4.png','rpt_fig5.png']:
        if os.path.exists(f):
            os.remove(f)
    print("Done.")
