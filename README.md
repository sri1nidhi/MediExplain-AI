# 🩺 MediExplain AI

AI-powered Medical Report Analyzer that converts complex medical reports into simple, patient-friendly explanations in multiple Indian languages.

## 🚀 Problem Statement

Medical reports are difficult for non-medical users to understand.

Patients often struggle to:

* Understand medical terminology
* Identify abnormal findings
* Know the severity of issues
* Ask relevant questions to doctors
* Understand reports in their native language

MediExplain AI solves this problem using Generative AI.

---

## ✨ Features

### 📄 Multiple Report Upload Options

* Upload PDF medical reports
* Upload report images (JPG, JPEG, PNG)

### 🤖 AI Medical Analysis

Supports analysis of:

* Blood Reports
* CBC Reports
* Thyroid Reports
* Kidney Function Reports
* Liver Function Reports
* Urine Reports
* MRI Reports
* CT Scan Reports
* X-Ray Reports
* Discharge Summaries
* Prescription Documents
* General Hospital Reports

### 📊 Health Risk Dashboard

Displays:

* 🔴 High Risk Findings
* 🟠 Moderate Risk Findings
* 🟢 Normal Findings

### 🩺 Patient-Friendly Summary

Converts technical medical information into easy-to-understand language.

### ⚠️ Abnormal Findings Detection

Highlights:

* Abnormal values
* Possible implications
* Risk indicators

### 🧪 Test Results Breakdown

Provides section-wise explanations for report parameters.

Example:

* Hemoglobin
* RBC Count
* WBC Count
* Platelets
* Thyroid Levels
* Cholesterol Levels

Each section includes:

* Test Value
* Normal Range
* Risk Level
* Explanation

### 🌐 Multi-Language Support

Supports:

* English
* Telugu
* Hindi

### 👨‍⚕️ Questions to Ask Doctor

Generates meaningful questions patients can discuss with healthcare professionals.

### 📋 Health Recommendations

Provides general lifestyle and health recommendations.

### 📥 Download Analysis

Users can download the generated report summary.

### 🔑 BYOK (Bring Your Own Key)

Users can provide their own Gemini API key.

Benefits:

* No API cost for deployment
* Privacy-friendly
* Mentor-recommended feature

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### AI

* Google Gemini 2.5 Flash
* LangChain

### Document Processing

* PyMuPDF

### OCR (Image Reports)

* Pillow
* Tesseract OCR

### Backend

* Python

---

## 📂 Project Structure

```text
MediExplain-AI/
│
├── app.py
├── requirements.txt
├── runtime.txt
│
├── utils/
│   ├── __init__.py
│   ├── llm.py
│   ├── pdf_loader.py
│   └── image_loader.py
│
└── README.md
```

---

## ▶️ Run Locally

### Clone Repository

```bash
git clone https://github.com/sri1nidhi/MediExplain-AI.git
cd MediExplain-AI
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## 🔮 Future Scope

* Offline AI using Ollama
* Additional Indian languages
* Voice-based explanation
* Hospital integration
* Medical history tracking
* Doctor recommendation system

---

## ⚠️ Disclaimer

This project is intended for educational and informational purposes only.

It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a licensed healthcare professional regarding medical decisions.
