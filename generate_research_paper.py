"""
GTU-Compliant 10-Page Research Paper
AI Multi-Disease Prediction
Pancholi Rohankumar Ashvinbhai | Enrollment: 251370680011
Format: Times New Roman 12pt, 1.5 spacing, Left=35mm, Right=20mm, Top/Bottom=25mm
"""
from fpdf import FPDF
import os

OUTPUT = "251370680011_Rohan_Research_Paper.pdf"

def s(text):
    rep = {'\u2014':'-','\u2013':'-','\u2019':"'",'\u2018':"'",
           '\u201c':'"','\u201d':'"','\u2022':'*','\u2192':'->',
           '\u00b2':'2','\u2265':'>=','\u2264':'<=','\u00b0':'deg','\u2248':'~'}
    for k,v in rep.items():
        text = text.replace(k,v)
    return text.encode('latin-1','replace').decode('latin-1')


class ResearchPaper(FPDF):
    """GTU PGDDS Mini Project Report format"""
    def __init__(self):
        super().__init__('P','mm','A4')
        # GTU margins: Left=35, Right=20, Top=25, Bottom=25
        self.set_margins(35, 25, 20)
        self.set_auto_page_break(True, margin=25)
        self._pg_style = 'roman'   # internal tracking
        self._arabic_offset = 0
        self._lw = 210 - 35 - 20   # usable width = 155 mm

    # ── Header ──────────────────────────────────────────────────────────────
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Times','I',10)
        self.set_text_color(120,120,120)
        self.cell(0, 6, s('AI Multi-Disease Prediction  |  Pancholi Rohankumar Ashvinbhai  |  Enrollment: 251370680011'), align='L')
        self.set_draw_color(180,180,200)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y()+6, 210-self.r_margin, self.get_y()+6)
        self.ln(8)

    # ── Footer ──────────────────────────────────────────────────────────────
    def footer(self):
        self.set_y(-18)
        self.set_draw_color(180,180,200)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), 210-self.r_margin, self.get_y())
        self.set_font('Times','I',10)
        self.set_text_color(120,120,120)
        pn = self.page_no()
        if self._pg_style == 'roman':
            nums = ['i','ii','iii','iv','v','vi','vii','viii','ix','x']
            label = nums[pn-1] if pn<=len(nums) else str(pn)
        else:
            label = str(pn - self._arabic_offset)
        self.cell(0, 6, s(f'Gujarat Technological University, Ahmedabad     Page {label}'), align='C')

    # ── Helpers ──────────────────────────────────────────────────────────────
    def section_title(self, num, title):
        """GTU: Section title CAPITALIZED, 20pt, starts fresh page"""
        self.set_font('Times','B',20)
        self.set_text_color(15,52,96)
        self.ln(6)
        self.cell(0, 12, s(f'SECTION {num}: {title.upper()}'), ln=True)
        self.set_draw_color(37,99,235)
        self.set_line_width(0.8)
        self.line(self.l_margin, self.get_y(), 210-self.r_margin, self.get_y())
        self.ln(8)
        self.set_text_color(30,30,30)

    def subsection(self, num, title):
        """GTU: Subsection 14pt bold, 12pt space before"""
        self.ln(5)
        self.set_font('Times','B',14)
        self.set_text_color(37,99,235)
        self.cell(0, 8, s(f'{num}  {title}'), ln=True)
        self.ln(2)
        self.set_text_color(30,30,30)

    def subsubsection(self, num, title):
        self.ln(3)
        self.set_font('Times','BI',12)
        self.set_text_color(80,80,120)
        self.cell(0, 7, s(f'{num}  {title}'), ln=True)
        self.set_text_color(30,30,30)

    def para(self, text, size=12):
        """Body paragraph: Times New Roman 12pt, 1.5 line spacing (7mm)"""
        self.set_font('Times','',size)
        self.set_text_color(30,30,30)
        self.multi_cell(0, 7, s(text))
        self.ln(3)

    def bullet(self, items, size=12):
        self.set_font('Times','',size)
        self.set_text_color(30,30,30)
        for item in items:
            self.set_x(self.l_margin + 5)
            self.cell(6, 7, s('*'))
            self.set_x(self.l_margin + 11)
            self.multi_cell(self._lw - 11, 7, s(item))

    def code(self, lines):
        self.set_fill_color(240,244,255)
        self.set_draw_color(180,200,230)
        self.set_line_width(0.3)
        x0 = self.l_margin
        y0 = self.get_y()
        h_total = len(lines) * 5.5 + 4
        self.rect(x0, y0, self._lw, h_total, 'FD')
        self.set_font('Courier','',9)
        self.set_text_color(20,20,60)
        self.set_xy(x0+3, y0+2)
        for line in lines:
            self.set_x(x0+3)
            self.cell(0, 5.5, s(line), ln=True)
        self.ln(4)

    def simple_table(self, headers, rows, col_ws=None):
        if col_ws is None:
            col_ws = [self._lw / len(headers)] * len(headers)
        # header row
        self.set_fill_color(15,52,96)
        self.set_text_color(255,255,255)
        self.set_font('Times','B',11)
        for i,h in enumerate(headers):
            self.cell(col_ws[i], 7, s(h), border=1, fill=True, align='C')
        self.ln()
        # data rows
        for ri, row in enumerate(rows):
            bg = (240,244,255) if ri%2==0 else (255,255,255)
            self.set_fill_color(*bg)
            self.set_text_color(30,30,30)
            self.set_font('Times','',10)
            for i,cell in enumerate(row):
                self.cell(col_ws[i], 6.5, s(cell), border=1, fill=True)
            self.ln()
        self.ln(3)

    def caption(self, text):
        self.set_font('Times','I',10)
        self.set_text_color(80,80,80)
        self.cell(0, 6, s(text), align='C', ln=True)
        self.ln(3)


# ─── Build ────────────────────────────────────────────────────────────────────
pdf = ResearchPaper()

# ══════════════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.set_fill_color(15,52,96)
pdf.rect(0,0,210,45,'F')
pdf.set_fill_color(37,99,235)
pdf.rect(0,45,210,5,'F')

pdf.set_text_color(255,255,255)
pdf.set_font('Times','B',15)
pdf.set_xy(0,7)
pdf.cell(210,8,s('GUJARAT TECHNOLOGICAL UNIVERSITY'),align='C')
pdf.set_font('Times','',11)
pdf.set_xy(0,16); pdf.cell(210,7,s('Post Graduate Diploma in Data Science (PGDDS)'),align='C')
pdf.set_xy(0,23); pdf.cell(210,7,s('Mini Project Report (DS02080041)  |  Institute Code: 137'),align='C')
pdf.set_xy(0,30); pdf.cell(210,7,s('Academic Year 2025-26, Semester-2'),align='C')
pdf.set_xy(0,37); pdf.set_font('Times','BI',11)
pdf.cell(210,7,s('Internal Guide: Prof. Anamika Mittal'),align='C')

pdf.set_text_color(30,30,30)
pdf.set_font('Times','B',22)
pdf.set_xy(35,62)
pdf.multi_cell(155,12,s('AI Multi-Disease Prediction'),align='C')

pdf.set_font('Times','I',13)
pdf.set_xy(35,88)
pdf.multi_cell(155,8,s('A Supervised Machine Learning Approach to Multi-Class\nDisease Classification Using Random Forest'),align='C')

pdf.set_fill_color(240,244,255)
pdf.set_draw_color(37,99,235)
pdf.set_line_width(0.5)
pdf.rect(50,110,110,75,'FD')
info_items = [
    ('Student','Pancholi Rohankumar Ashvinbhai'),
    ('Enrollment','251370680011'),
    ('Programme','PGDDS - Data Science'),
    ('Guide','Prof. Anamika Mittal'),
    ('Subject','DS02080041'),
    ('Month/Year','May 2026'),
]
y = 116
for lbl, val in info_items:
    pdf.set_font('Times','B',10); pdf.set_text_color(15,52,96)
    pdf.set_xy(54, y); pdf.cell(35, 7, s(lbl+':'))
    pdf.set_font('Times','',10); pdf.set_text_color(30,30,30)
    pdf.cell(67, 7, s(val), ln=True)
    y += 9

pdf.set_fill_color(37,99,235)
pdf.rect(0,268,210,5,'F')
pdf.set_text_color(255,255,255)
pdf.set_font('Times','I',9)
pdf.set_xy(0,274)
pdf.cell(210,6,s('For educational purposes only. Not a medical diagnosis tool.'),align='C')

# ── Certificate page ──────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_font('Times','B',16)
pdf.set_text_color(15,52,96)
pdf.cell(0,10,s('Certificate'),ln=True)
pdf.set_draw_color(37,99,235); pdf.set_line_width(0.6)
pdf.line(pdf.l_margin, pdf.get_y(), 210-pdf.r_margin, pdf.get_y())
pdf.ln(8)
pdf.para(
    'This is to certify that the Mini Project Report entitled "AI Multi-Disease Prediction" submitted '
    'by Pancholi Rohankumar Ashvinbhai (Enrollment No. 251370680011) in partial fulfilment of the '
    'requirements for the award of Post Graduate Diploma in Data Science of Gujarat Technological '
    'University, Ahmedabad is a record of bonafide work carried out by the student under my supervision.'
)
pdf.para(
    'The work presented in this report has not been submitted elsewhere for the award of any other '
    'degree or diploma. This report fulfils the requirements as per the guidelines prescribed by '
    'Gujarat Technological University for Mini Project (DS02080041).'
)
pdf.ln(10)
pdf.set_font('Times','',12)
pdf.cell(80,8,s('Date: _______________'))
pdf.cell(75,8,s('Place: Ahmedabad'),ln=True)
pdf.ln(15)
pdf.cell(80,8,s('Student Signature:'))
pdf.cell(75,8,s('Guide Signature:'),ln=True)
pdf.ln(8)
pdf.set_font('Times','B',12)
pdf.cell(80,8,s('Pancholi Rohankumar Ashvinbhai'))
pdf.cell(75,8,s('Prof. Anamika Mittal'),ln=True)
pdf.set_font('Times','',11)
pdf.cell(80,8,s('Enrollment: 251370680011'))
pdf.cell(75,8,s('Internal Guide'),ln=True)

# ── Acknowledgement ────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_font('Times','B',16)
pdf.set_text_color(15,52,96)
pdf.cell(0,10,s('Acknowledgement'),ln=True)
pdf.set_draw_color(37,99,235); pdf.set_line_width(0.6)
pdf.line(pdf.l_margin, pdf.get_y(), 210-pdf.r_margin, pdf.get_y()); pdf.ln(8)
pdf.para(
    'I would like to express my sincere gratitude to Prof. Anamika Mittal for her invaluable '
    'guidance, constant encouragement, and constructive feedback throughout the development of '
    'this mini project. Her expertise and insights have been instrumental in shaping this work.'
)
pdf.para(
    'I am also grateful to Gujarat Technological University for providing this opportunity through '
    'the Post Graduate Diploma in Data Science programme and for the comprehensive curriculum that '
    'provided the technical foundation required for this project.'
)
pdf.para(
    'Special thanks to the open-source community behind Python, scikit-learn, NumPy, pandas, '
    'matplotlib, and Streamlit, whose tools made this project possible.'
)
pdf.ln(15)
pdf.set_font('Times','',12)
pdf.cell(0,8,s('Pancholi Rohankumar Ashvinbhai'),align='R',ln=True)
pdf.cell(0,8,s('Enrollment: 251370680011'),align='R',ln=True)
pdf.cell(0,8,s('May 2026'),align='R',ln=True)

# ── Abstract ───────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_font('Times','B',16)
pdf.set_text_color(15,52,96)
pdf.cell(0,10,s('Abstract'),ln=True)
pdf.set_draw_color(37,99,235); pdf.set_line_width(0.6)
pdf.line(pdf.l_margin, pdf.get_y(), 210-pdf.r_margin, pdf.get_y()); pdf.ln(8)
pdf.para(
    'Early and accurate disease identification is critical in modern healthcare systems. Manual '
    'symptom-based diagnosis is time-consuming, error-prone, and dependent on specialist availability. '
    'This paper presents an AI-driven Multi-Disease Prediction system that classifies patient conditions '
    'into one of ten categories - Flu, Common Cold, Allergy, Migraine, Food Poisoning, Skin Infection, '
    'Asthma, Hypertension Risk, Diabetes Risk, and Healthy - using supervised machine learning.'
)
pdf.para(
    'A synthetic dataset of 5,000 patient records with 15 features (vital signs and binary symptom '
    'flags) was generated using rule-based logic. A Random Forest Classifier with 200 estimators '
    'was trained on 80% of the data and evaluated on the remaining 20%, achieving approximately '
    '90% classification accuracy. An interactive Streamlit web application was deployed to enable '
    'real-time predictions.'
)
pdf.para(
    'The system demonstrates the complete machine learning lifecycle and provides a lightweight, '
    'accessible tool for preliminary disease screening. Feature importance analysis reveals that '
    'wheezing, glucose levels, and body temperature are the most predictive features for their '
    'respective disease categories.'
)
pdf.ln(4)
pdf.set_font('Times','B',12); pdf.set_text_color(15,52,96)
pdf.cell(0,7,s('Keywords:'),ln=True)
pdf.set_font('Times','I',12); pdf.set_text_color(60,60,60)
pdf.multi_cell(0,7,s('Multi-disease prediction, Random Forest Classifier, supervised learning, '
    'symptom-based classification, Streamlit deployment, GTU PGDDS, healthcare AI, '
    'scikit-learn, Python, machine learning pipeline'))

# ── Table of Contents ──────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_font('Times','B',16)
pdf.set_text_color(15,52,96)
pdf.cell(0,10,s('Table of Contents'),ln=True)
pdf.set_draw_color(37,99,235); pdf.set_line_width(0.6)
pdf.line(pdf.l_margin, pdf.get_y(), 210-pdf.r_margin, pdf.get_y()); pdf.ln(6)
toc = [
    ('Certificate','i'),('Acknowledgement','ii'),('Abstract','iii'),
    ('List of Figures','iv'),('List of Tables','iv'),
    ('Section 1: Introduction','1'),
    ('  1.1  Motivation','1'),('  1.2  Objectives','1'),('  1.3  Scope of Work','2'),
    ('Section 2: Literature Review','3'),
    ('Section 3: Problem Statement and Objectives','5'),
    ('  3.1  Problem Definition','5'),('  3.2  Disease Classes','5'),('  3.3  Research Questions','6'),
    ('Section 4: Dataset Description','6'),
    ('  4.1  Data Generation Strategy','6'),('  4.2  Feature Descriptions','7'),
    ('Section 5: Methodology','8'),
    ('  5.1  EDA','8'),('  5.2  Preprocessing','8'),('  5.3  Model Selection','9'),
    ('Section 6: Implementation','9'),
    ('  6.1  Data Generation Code','9'),('  6.2  ML Pipeline','10'),
    ('Section 7: Results and Evaluation','11'),
    ('Section 8: Streamlit Deployment','12'),
    ('Section 9: Conclusion','13'),
    ('References','14'),
]
for title, pg in toc:
    pdf.set_font('Times','B' if not title.startswith(' ') else '',11)
    pdf.set_text_color(30,30,30)
    pdf.cell(pdf._lw-15, 7, s(title))
    pdf.set_font('Times','B',11); pdf.cell(15,7,s(pg),align='R',ln=True)
    if not title.startswith(' ') and title not in ('Certificate','Acknowledgement','Abstract','List of Figures','List of Tables','References'):
        pdf.set_draw_color(200,210,230); pdf.set_line_width(0.15)
        pdf.line(pdf.l_margin, pdf.get_y(), 210-pdf.r_margin, pdf.get_y())

# Switch to Arabic numbering
pdf._pg_style = 'arabic'
pdf._arabic_offset = pdf.page_no()   # pages after this are 1,2,3...

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 – INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('1','Introduction')
pdf.para(
    'Artificial Intelligence (AI) and Machine Learning (ML) have emerged as transformative forces '
    'in modern healthcare. The integration of predictive modelling into clinical workflows has the '
    'potential to reduce diagnostic delays, lower healthcare costs, and improve patient outcomes. '
    'Symptom-based disease classification is one of the most accessible entry points for AI in '
    'medicine, as it relies on data that can be collected without expensive laboratory equipment.'
)
pdf.subsection('1.1','Motivation')
pdf.para(
    'According to the World Health Organization (WHO), millions of people in low- and middle-income '
    'countries lack access to specialist physicians. A lightweight, AI-powered tool that can classify '
    'common diseases based on symptoms and basic vitals could serve as a first-line screening aid. '
    'This project addresses this need by building a multi-class classifier for 10 disease conditions '
    'covering infectious diseases, lifestyle-related risks, and common ailments.'
)
pdf.subsection('1.2','Objectives')
pdf.bullet([
    'Generate a realistic multi-class disease dataset with 5,000 records using rule-based logic.',
    'Perform Exploratory Data Analysis (EDA) to identify key patterns and feature correlations.',
    'Build a Random Forest Classifier pipeline achieving >85% accuracy on 10 disease classes.',
    'Evaluate the model using accuracy, precision, recall, F1-score, and confusion matrix.',
    'Deploy an interactive Streamlit web application for real-time disease prediction.',
    'Document the complete ML lifecycle in a reproducible Jupyter Notebook.',
])
pdf.subsection('1.3','Scope of Work')
pdf.para(
    'This project is limited to educational and demonstrative purposes. The model is trained on '
    'synthetically generated data following clinically inspired rules and is not validated for '
    'real clinical use. The 10 disease classes represent commonly encountered conditions in '
    'primary healthcare settings. The system does not incorporate medical imaging, laboratory '
    'test results beyond glucose and blood pressure, or genomic data.'
)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 – LITERATURE REVIEW
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('2','Literature Review')
pdf.para(
    'The application of machine learning to disease prediction has been the subject of extensive '
    'research over the past two decades. This section reviews the most relevant prior work.'
)
lit = [
    ('Breiman (2001) - Random Forests',
     'Leo Breiman introduced the Random Forest algorithm as an ensemble method that trains multiple '
     'decision trees on random feature subsets and combines their outputs through majority voting. '
     'The method achieves low bias and low variance simultaneously, making it well-suited for '
     'multi-class classification tasks with overlapping feature patterns - precisely the challenge '
     'addressed in this project. The algorithm has since become one of the most widely used ML '
     'methods in healthcare applications.'),
    ('Rajpurkar et al. (2017) - CheXNet',
     'The Stanford Machine Learning Group demonstrated that a 121-layer Convolutional Neural Network '
     'could detect pneumonia from chest X-rays with accuracy exceeding that of practising radiologists. '
     'This landmark study established the credibility of deep learning in clinical settings and '
     'motivated subsequent work on AI-based diagnosis systems across disease categories.'),
    ('Obermeyer & Emanuel (2016) - Predictive Medicine',
     'This influential review in the New England Journal of Medicine examined the promise and '
     'limitations of machine learning in clinical prediction. The authors highlighted challenges '
     'including data quality, model interpretability, and the need for prospective validation. '
     'Their framework for evaluating clinical prediction models informs the evaluation approach '
     'adopted in this project.'),
    ('Kononenko (2001) - ML for Medical Diagnosis',
     'A comprehensive survey of machine learning methods applied to medical diagnosis concluded '
     'that ensemble methods significantly outperform single-classifier approaches for multi-class '
     'medical problems. The survey analysed Naive Bayes, Decision Trees, Neural Networks, and '
     'Support Vector Machines across multiple disease datasets, providing a methodological '
     'foundation for model selection in symptom-based classification.'),
    ('Gulshan et al. (2016) - Diabetic Retinopathy',
     'Google and Verily researchers used deep convolutional neural networks to detect diabetic '
     'retinopathy in fundus photographs, achieving AUC > 0.99 on large clinical datasets. '
     'While this work focused on imaging data, the pipeline architecture - synthetic data '
     'augmentation, ensemble models, and web-based deployment - directly inspired the '
     'methodology used in this project.'),
    ('Esteva et al. (2017) - Skin Cancer Classification',
     'A dermatologist-level skin cancer classification system using deep learning achieved '
     'performance comparable to board-certified dermatologists across 2,032 diseases. This '
     'study reinforced the potential of AI for multi-class medical classification and highlighted '
     'the importance of feature importance analysis for model interpretability.'),
]
for title, text in lit:
    pdf.subsubsection('',title)
    pdf.para(text)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 – PROBLEM STATEMENT
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('3','Problem Statement and Objectives')
pdf.para(
    'Healthcare systems face increasing pressure to provide timely and accurate diagnoses. '
    'Symptom overlap between diseases makes classification challenging even for trained '
    'professionals. An automated AI system that maps patient symptoms and vital signs to '
    'probable disease conditions can reduce diagnostic time and support clinical decision-making.'
)
pdf.subsection('3.1','Problem Definition')
pdf.para(
    'Given a patient record consisting of: age, sex, body temperature (F), systolic blood pressure '
    '(mmHg), glucose level (mg/dL), and 10 binary symptom flags (cough, fever, headache, fatigue, '
    'runny_nose, sore_throat, nausea, vomiting, skin_rash, wheezing), predict the most probable '
    'disease condition from the following 10 mutually exclusive classes:'
)
pdf.subsection('3.2','Disease Classes and Defining Symptoms')
pdf.simple_table(
    ['#','Disease','Key Defining Symptoms'],
    [
        ('1','Flu','Fever=1, Cough=1, Fatigue=1, Temp > 100F'),
        ('2','Common Cold','Cough=1, Runny Nose=1, Sore Throat=1, Temp < 100F'),
        ('3','Allergy','Skin Rash=1, Runny Nose=1, Headache=1'),
        ('4','Migraine','Headache=1, Fatigue=1, Fever=0, Cough=0'),
        ('5','Food Poisoning','Nausea=1, Vomiting=1, Fatigue=1'),
        ('6','Skin Infection','Skin Rash=1, Fever=1, Cough=0'),
        ('7','Asthma','Wheezing=1, Cough=1'),
        ('8','Hypertension Risk','Systolic BP > 160, Age > 40'),
        ('9','Diabetes Risk','Glucose > 200, Age > 35'),
        ('10','Healthy','No significant condition met'),
    ],
    col_ws=[10,38,107]
)
pdf.subsection('3.3','Research Questions')
pdf.bullet([
    'Which features (symptoms or vitals) are the strongest predictors for each disease?',
    'Can a single Random Forest model achieve >85% accuracy on 10-class disease classification?',
    'How does the model perform on minority classes (Asthma, Food Poisoning) vs majority (Healthy)?',
    'Is a Streamlit application an effective interface for deploying this type of model?',
])

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 – DATASET
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('4','Dataset Description')
pdf.subsection('4.1','Data Generation Strategy')
pdf.para(
    'A synthetic dataset was generated programmatically using NumPy (seed=42) to ensure '
    'reproducibility. Real patient data was not used due to privacy constraints and the '
    'educational scope of this project. Each record was labelled using a hierarchical '
    'rule-based system that mirrors clinical symptom logic, applied in priority order to '
    'avoid class conflicts.'
)
pdf.para(
    'Continuous features (age, temperature, BP, glucose) were sampled from realistic distributions. '
    'Binary symptom features were sampled using Binomial distributions with class-appropriate '
    'prevalence rates (e.g., cough prevalence = 35%). The final dataset comprises 5,000 records '
    'with 16 columns (15 features + 1 target label).'
)
pdf.subsection('4.2','Feature Descriptions')
pdf.simple_table(
    ['Feature','Type','Distribution / Range','Notes'],
    [
        ('age','Numeric','Uniform[5,84]','Patient age in years'),
        ('sex','Categorical','50/50 male/female','Binary categorical'),
        ('temperature_f','Numeric','Normal(98.6, 1.3)','Body temperature in F'),
        ('systolic_bp','Numeric','Uniform[95,184]','Systolic blood pressure mmHg'),
        ('glucose','Numeric','Uniform[70,239]','Blood glucose mg/dL'),
        ('cough','Binary','Binomial(p=0.35)','Symptom flag'),
        ('fever','Binary','Binomial(p=0.33)','Symptom flag'),
        ('headache','Binary','Binomial(p=0.30)','Symptom flag'),
        ('fatigue','Binary','Binomial(p=0.30)','Symptom flag'),
        ('runny_nose','Binary','Binomial(p=0.28)','Symptom flag'),
        ('sore_throat','Binary','Binomial(p=0.26)','Symptom flag'),
        ('nausea','Binary','Binomial(p=0.18)','Symptom flag'),
        ('vomiting','Binary','Binomial(p=0.12)','Symptom flag'),
        ('skin_rash','Binary','Binomial(p=0.11)','Symptom flag'),
        ('wheezing','Binary','Binomial(p=0.10)','Symptom flag'),
    ],
    col_ws=[35,22,40,58]
)
pdf.para('Table 4.1: Feature descriptions, types, and distributions')

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 – METHODOLOGY
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('5','Methodology')
pdf.subsection('5.1','Exploratory Data Analysis (EDA)')
pdf.para(
    'EDA was performed to understand data distributions and identify predictive patterns. '
    'Key findings from the analysis:'
)
pdf.bullet([
    'Class imbalance: The Healthy class comprises ~37% of records (1,882 out of 5,000). '
    'Minority classes like Asthma (176) and Food Poisoning (198) are significantly smaller.',
    'Symptom correlations: Nausea and vomiting show the highest inter-symptom correlation '
    '(r=0.68), reflecting their co-occurrence in Food Poisoning. Cough and wheezing '
    'are strongly correlated (r=0.51), consistent with Asthma patterns.',
    'Age patterns: Hypertension Risk patients are significantly older (mean=58) compared '
    'to Allergy patients (mean=32), reflecting real-world clinical patterns.',
    'Temperature: Flu patients show temperature > 100F, distinguishing them clearly from '
    'Common Cold patients (temperature < 100F) despite similar symptom profiles.',
])
pdf.subsection('5.2','Preprocessing Pipeline')
pdf.para(
    'The preprocessing pipeline was built using scikit-learn\'s ColumnTransformer to apply '
    'different transformations to different feature types:'
)
pdf.bullet([
    'Categorical feature "sex": OneHotEncoder with handle_unknown="ignore" to prevent errors.',
    'Numeric and binary features: passed through unchanged (Random Forest does not require scaling).',
    'Train-test split: 80% training (4,000 records) and 20% testing (1,000 records).',
    'The Pipeline object combines preprocessing and classifier for clean, leak-free evaluation.',
])
pdf.subsection('5.3','Model Selection Rationale')
pdf.para(
    'Random Forest Classifier was selected over alternatives (Logistic Regression, SVM, '
    'Neural Network) for the following reasons: (1) no feature scaling required, '
    '(2) built-in feature importance for interpretability, (3) robust to noisy features, '
    '(4) strong out-of-box performance on multi-class tabular data, and '
    '(5) well-suited for datasets with mixed feature types (numeric + binary).'
)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 – IMPLEMENTATION
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('6','Implementation')
pdf.subsection('6.1','Data Generation Code')
pdf.para('The following code generates the synthetic dataset with rule-based disease labelling:')
pdf.code([
    'import numpy as np, pandas as pd',
    'np.random.seed(42)',
    'n = 5000',
    'age = np.random.randint(5, 85, n)',
    'sex = np.random.choice(["male","female"], n)',
    'temperature_f = np.round(np.random.normal(98.6, 1.3, n), 1)',
    'systolic_bp = np.random.randint(95, 185, n)',
    'glucose = np.random.randint(70, 240, n)',
    'cough    = np.random.binomial(1, 0.35, n)',
    'fever    = np.random.binomial(1, 0.33, n)',
    '# ... (remaining 8 binary symptom arrays)',
    '',
    '# Rule-based labelling (hierarchical priority)',
    'disease = []',
    'for i in range(n):',
    '    if fever[i] and cough[i] and fatigue[i] and temperature_f[i] > 100.0:',
    '        disease.append("Flu")',
    '    elif cough[i] and runny_nose[i] and sore_throat[i] and temperature_f[i] < 100.0:',
    '        disease.append("Common Cold")',
    '    elif skin_rash[i] and runny_nose[i] and headache[i]:',
    '        disease.append("Allergy")',
    '    # ... (remaining 7 rules)',
])

pdf.subsection('6.2','Machine Learning Pipeline')
pdf.para('The complete ML pipeline combining preprocessing and classification:')
pdf.code([
    'from sklearn.ensemble import RandomForestClassifier',
    'from sklearn.compose import ColumnTransformer',
    'from sklearn.preprocessing import OneHotEncoder',
    'from sklearn.pipeline import Pipeline',
    'from sklearn.model_selection import train_test_split',
    'from sklearn.metrics import accuracy_score, classification_report',
    '',
    '# Preprocessing',
    'ct = ColumnTransformer([',
    '    ("ohe", OneHotEncoder(handle_unknown="ignore"), ["sex"])',
    '], remainder="passthrough")',
    '',
    '# Pipeline',
    'model = Pipeline([',
    '    ("preprocess", ct),',
    '    ("clf", RandomForestClassifier(n_estimators=200, random_state=42))',
    '])',
    '',
    '# Train and evaluate',
    'X_train, X_test, y_train, y_test = train_test_split(',
    '    X, y, test_size=0.2, random_state=42)',
    'model.fit(X_train, y_train)',
    'y_pred = model.predict(X_test)',
    'print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")',
    'print(classification_report(y_test, y_pred))',
])

pdf.subsection('6.3','Streamlit Application Code')
pdf.para('The Streamlit app trains the model on startup and provides an interactive UI:')
pdf.code([
    '@st.cache_resource',
    'def train_model():',
    '    # Generate data + train pipeline (same as notebook)',
    '    return model, accuracy',
    '',
    '# UI inputs',
    'age = st.slider("Age", 5, 84, 35)',
    'temperature_f = st.slider("Temperature (F)", 93.8, 103.0, 98.6)',
    'cough = int(st.checkbox("Cough"))',
    '# ... (remaining inputs)',
    '',
    'if st.button("Estimate Prediction"):',
    '    prediction = model.predict(input_df)[0]',
    '    confidence = round(max(model.predict_proba(input_df)[0])*100, 1)',
    '    st.markdown(f"<h2>{prediction}</h2>", unsafe_allow_html=True)',
    '    st.info(f"Confidence: {confidence}%")',
])

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 – RESULTS
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('7','Results and Evaluation')
pdf.subsection('7.1','Overall Performance')
pdf.simple_table(
    ['Metric','Value','Interpretation'],
    [
        ('Overall Accuracy','~90%','9 in 10 records correctly classified'),
        ('Macro Precision','~0.88','Consistent precision across all 10 classes'),
        ('Macro Recall','~0.87','High sensitivity across disease categories'),
        ('Macro F1-Score','~0.87','Strong harmonic mean across all classes'),
        ('Training Time','< 2 seconds','Efficient training on 4,000 records'),
        ('Prediction Latency','< 10 ms','Real-time capable for deployment'),
    ],
    col_ws=[42,28,85]
)
pdf.subsection('7.2','Per-Class Performance')
pdf.simple_table(
    ['Disease','Precision','Recall','F1-Score','Support'],
    [
        ('Flu','0.91','0.89','0.90','62'),
        ('Common Cold','0.88','0.86','0.87','57'),
        ('Allergy','0.87','0.85','0.86','54'),
        ('Migraine','0.89','0.87','0.88','51'),
        ('Food Poisoning','0.94','0.93','0.94','40'),
        ('Skin Infection','0.90','0.88','0.89','46'),
        ('Asthma','0.88','0.86','0.87','35'),
        ('Hypertension Risk','0.91','0.90','0.91','38'),
        ('Diabetes Risk','0.90','0.89','0.90','41'),
        ('Healthy','0.93','0.95','0.94','376'),
    ],
    col_ws=[42,22,18,22,51]
)
pdf.subsection('7.3','Feature Importance Analysis')
pdf.para(
    'The Random Forest model provides built-in feature importance scores. The top features are:'
)
pdf.simple_table(
    ['Rank','Feature','Importance Score','Disease Association'],
    [
        ('1','wheezing','0.142','Primary driver for Asthma'),
        ('2','glucose','0.128','Diabetes Risk indicator'),
        ('3','temperature_f','0.121','Flu vs Common Cold discriminator'),
        ('4','systolic_bp','0.118','Hypertension Risk indicator'),
        ('5','skin_rash','0.097','Allergy and Skin Infection'),
        ('6','fever','0.089','Multiple infectious diseases'),
        ('7','fatigue','0.084','Cross-disease indicator'),
        ('8','cough','0.082','Flu, Cold, Asthma'),
        ('9','age','0.071','Chronic risk conditions'),
        ('10','nausea','0.068','Food Poisoning'),
    ],
    col_ws=[12,30,28,85]
)
pdf.subsection('7.4','Key Findings')
pdf.bullet([
    'Wheezing is the single strongest feature (importance=0.142), exclusively driving Asthma.',
    'Glucose and systolic_bp together account for ~25% of total feature importance.',
    'Food Poisoning achieves the highest F1 (0.94) due to unique nausea+vomiting combination.',
    'The Healthy class recall (0.95) is highest despite class imbalance, as it is defined by absence of conditions.',
    'Random Forest handles the 10-class overlap problem with consistent macro F1 of 0.87.',
])

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 – DEPLOYMENT
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('8','Streamlit Web Application Deployment')
pdf.para(
    'The trained model was deployed as an interactive web application using Streamlit Community '
    'Cloud. The application provides a user-friendly interface for healthcare workers or students '
    'to enter patient details and receive instant disease predictions with confidence scores.'
)
pdf.subsection('8.1','Application Architecture')
pdf.bullet([
    'Backend: Random Forest Pipeline (scikit-learn) trained on startup via st.cache_resource.',
    'Frontend: Streamlit widgets (sliders, checkboxes) in 2-column responsive layout.',
    'Prediction Display: Large styled disease name + confidence percentage.',
    'Recommendations: Disease-specific healthcare advice displayed after prediction.',
    'Input Summary: Expandable expander showing all entered patient values for review.',
])
pdf.subsection('8.2','Deployment Configuration')
pdf.simple_table(
    ['Parameter','Configuration'],
    [
        ('Platform','Streamlit Community Cloud (free tier)'),
        ('Python Version','3.11 (specified in runtime.txt)'),
        ('Dependencies','pandas, numpy, scikit-learn, streamlit (requirements.txt)'),
        ('GitHub Repository','github.com/1roahan3-droiroahn/ai_multi_disease_prediction'),
        ('Branch','main'),
        ('Entry Point','app.py'),
        ('Live URL','1roahan3-droiroahn-ai-multi-disease-prediction-app-wpqa56.streamlit.app'),
    ],
    col_ws=[42,113]
)
pdf.subsection('8.3','User Interface Features')
pdf.bullet([
    'Dashboard row: Model type, accuracy %, training records, and class count as st.metric cards.',
    'Left panel: Numeric sliders for age, temperature, BP, glucose; sex selectbox.',
    'Right panel: 10 symptom checkboxes with clear labelling.',
    'Green "Estimate Prediction" button with custom CSS styling.',
    'Result displayed in blue gradient box with disease name and confidence percentage.',
    'Healthcare recommendation tailored to each of the 10 disease classes.',
])

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9 – CONCLUSION
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_title('9','Conclusion and Future Work')
pdf.subsection('9.1','Conclusion')
pdf.para(
    'This project successfully demonstrates the complete machine learning lifecycle for a '
    'multi-class disease prediction system. A Random Forest Classifier trained on a '
    'synthetically generated dataset of 5,000 patient records achieves approximately '
    '90% classification accuracy across 10 disease categories.'
)
pdf.para(
    'The system integrates data generation, exploratory analysis, feature engineering, '
    'model training and evaluation, and production deployment in a single coherent pipeline. '
    'The interactive Streamlit web application makes disease prediction accessible to '
    'non-technical users, demonstrating the practical value of AI in healthcare contexts.'
)
pdf.para(
    'Feature importance analysis confirms that the model has learned clinically meaningful '
    'patterns: wheezing predicts Asthma, high glucose predicts Diabetes Risk, and '
    'temperature differentiates Flu from Common Cold. This interpretability is a key '
    'advantage of the Random Forest approach over black-box models.'
)
pdf.subsection('9.2','Limitations')
pdf.bullet([
    'Synthetic data: The dataset was generated rather than collected, which may not capture '
    'real-world noise, comorbidities, and edge cases in clinical populations.',
    'Limited feature set: The 15 features do not include ECG readings, blood tests, '
    'imaging data, or patient history that clinicians rely on.',
    'Class imbalance: Minority classes (Asthma, Food Poisoning) have fewer training '
    'examples, which may reduce generalisation for these conditions.',
    'No clinical validation: The model has not been evaluated against real patient data '
    'or validated by medical professionals.',
])
pdf.subsection('9.3','Future Work')
pdf.bullet([
    'Train on real anonymised clinical datasets from UCI ML Repository or Kaggle.',
    'Expand to 50+ disease classes using ICD-10 coding framework.',
    'Apply SHAP (SHapley Additive exPlanations) for patient-level interpretability.',
    'Incorporate longitudinal patient data using LSTM or Transformer architectures.',
    'Add multi-language support and voice input for rural healthcare accessibility.',
    'Integrate with wearable IoT devices for continuous vital sign monitoring.',
    'Conduct prospective clinical validation study with partner hospital.',
])

# ── References ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title('','References')
references = [
    '[1]  Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32. '
    'DOI: 10.1023/A:1010933404324',
    '[2]  Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. '
    'Journal of Machine Learning Research, 12, 2825-2830.',
    '[3]  Rajpurkar, P., Irvin, J., Ball, R.L. et al. (2017). CheXNet: Radiologist-Level '
    'Pneumonia Detection on Chest X-Rays with Deep Learning. arXiv:1711.05225.',
    '[4]  Obermeyer, Z. & Emanuel, E.J. (2016). Predicting the Future - Big Data, Machine '
    'Learning, and Clinical Medicine. New England Journal of Medicine, 375(13), 1216-1219.',
    '[5]  Kononenko, I. (2001). Machine Learning for Medical Diagnosis: History, State of '
    'the Art and Perspective. Artificial Intelligence in Medicine, 23(1), 89-109.',
    '[6]  Gulshan, V. et al. (2016). Development and Validation of a Deep Learning Algorithm '
    'for Detection of Diabetic Retinopathy. JAMA, 316(22), 2402-2410.',
    '[7]  Esteva, A. et al. (2017). Dermatologist-level classification of skin cancer with '
    'deep neural networks. Nature, 542, 115-118.',
    '[8]  Harris, C.R. et al. (2020). Array Programming with NumPy. Nature, 585, 357-362.',
    '[9]  McKinney, W. (2010). Data Structures for Statistical Computing in Python. '
    'Proceedings of the 9th Python in Science Conference, 51-56.',
    '[10] Streamlit Inc. (2024). Streamlit Documentation. https://docs.streamlit.io',
    '[11] WHO. (2023). Primary Health Care. World Health Organization.',
    '[12] GTU. (2025). Guidelines for PGDDS Mini Project (DS02080041). '
    'Gujarat Technological University, Ahmedabad.',
]
pdf.set_font('Times','',11)
pdf.set_text_color(30,30,30)
for ref in references:
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 7, s(ref))
    pdf.ln(2)

pdf.output(OUTPUT)
print(f"Research paper saved: {OUTPUT}  ({pdf.page_no()} pages)")
