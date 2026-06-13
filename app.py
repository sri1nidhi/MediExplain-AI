import streamlit as st
from PIL import Image

from utils.pdf_loader import extract_pdf_text
from utils.llm import get_llm


st.set_page_config(
    page_title="MediExplain AI",
    page_icon="🩺",
    layout="wide"
)

# ---------------------------------------------------
# MULTILINGUAL UI
# ---------------------------------------------------

TEXT = {
    "English": {
        "title": "🩺 MediExplain AI",
        "subtitle": "Understand Medical Reports in Simple Language",
        "language": "🌐 Choose Language",
        "apikey": "🔑 Enter Gemini API Key",
        "upload": "📄 Upload Medical Report",
        "analyze": "🔍 Analyze Report",
        "success": "✅ Report Uploaded Successfully",
        "download": "📥 Download Analysis",
        "warning": "Please enter Gemini API Key",
        "disclaimer_title": "⚠️ Disclaimer",
        "disclaimer": """
This tool is for educational purposes only.

The generated analysis is NOT a medical diagnosis.

Please consult a qualified healthcare professional before making medical decisions.
"""
    },

    "Telugu": {
        "title": "🩺 మెడి ఎక్స్‌ప్లైన్ AI",
        "subtitle": "వైద్య నివేదికలను సులభమైన భాషలో అర్థం చేసుకోండి",
        "language": "🌐 భాషను ఎంచుకోండి",
        "apikey": "🔑 జెమినీ API కీ నమోదు చేయండి",
        "upload": "📄 వైద్య నివేదికను అప్‌లోడ్ చేయండి",
        "analyze": "🔍 నివేదికను విశ్లేషించండి",
        "success": "✅ నివేదిక విజయవంతంగా అప్‌లోడ్ చేయబడింది",
        "download": "📥 విశ్లేషణను డౌన్‌లోడ్ చేయండి",
        "warning": "దయచేసి Gemini API కీ నమోదు చేయండి",
        "disclaimer_title": "⚠️ హెచ్చరిక",
        "disclaimer": """
ఈ సాధనం విద్యా ప్రయోజనాల కోసం మాత్రమే.

ఇది వైద్య నిర్ధారణ కాదు.

వైద్య నిర్ణయాల కోసం అర్హత కలిగిన వైద్యుడిని సంప్రదించండి.
"""
    },

    "Hindi": {
        "title": "🩺 मेडीएक्सप्लेन AI",
        "subtitle": "मेडिकल रिपोर्ट को सरल भाषा में समझें",
        "language": "🌐 भाषा चुनें",
        "apikey": "🔑 जेमिनी API कुंजी दर्ज करें",
        "upload": "📄 मेडिकल रिपोर्ट अपलोड करें",
        "analyze": "🔍 रिपोर्ट का विश्लेषण करें",
        "success": "✅ रिपोर्ट सफलतापूर्वक अपलोड की गई",
        "download": "📥 विश्लेषण डाउनलोड करें",
        "warning": "कृपया Gemini API कुंजी दर्ज करें",
        "disclaimer_title": "⚠️ अस्वीकरण",
        "disclaimer": """
यह उपकरण केवल शैक्षणिक उद्देश्यों के लिए है।

यह कोई चिकित्सा निदान नहीं है।

किसी भी चिकित्सा निर्णय से पहले योग्य डॉक्टर से सलाह लें।
"""
    }
}

# ---------------------------------------------------
# LANGUAGE SELECTOR
# ---------------------------------------------------

language = st.selectbox(
    "🌐 Language",
    ["English", "Telugu", "Hindi"]
)

t = TEXT[language]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title(t["title"])
st.subheader(t["subtitle"])

# ---------------------------------------------------
# API KEY
# ---------------------------------------------------

api_key = st.text_input(
    t["apikey"],
    type="password"
)

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    t["upload"],
    type=["pdf", "png", "jpg", "jpeg"]
)

# ---------------------------------------------------
# PROCESS FILE
# ---------------------------------------------------

if uploaded_file:

    st.success(t["success"])

    is_pdf = uploaded_file.type == "application/pdf"

    if is_pdf:

        report_text = extract_pdf_text(uploaded_file)

    else:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Report",
            use_container_width=True
        )

    if not api_key:

        st.warning(t["warning"])
        st.stop()

    if st.button(t["analyze"]):

        with st.spinner("Analyzing Report..."):

            llm = get_llm(api_key)

            try:

                if is_pdf:

                    prompt = f"""
You are an expert medical report analyzer.

Analyze any hospital report.

Possible report types:

- Blood Report
- CBC Report
- Thyroid Report
- Kidney Report
- Liver Report
- Urine Report
- MRI Report
- CT Scan Report
- X-Ray Report
- Discharge Summary
- Prescription

Return markdown only.

# 📊 Health Risk Dashboard

Show:

🔴 High Risk Findings

🟠 Moderate Risk Findings

🟢 Normal Findings

# 🩺 Patient-Friendly Summary

Explain in simple language.

# ⚠️ Abnormal Findings

List abnormal values and explain them.

# 🧪 Test Results Breakdown

For every test parameter provide:

- Value
- Normal Range
- Risk Level
- Explanation

# 🌐 Explanation Language

Provide explanation in {language}

# 👨‍⚕️ Questions To Ask Doctor

Generate 5 questions.

# 📋 Health Recommendations

Provide recommendations.

Medical Report:

{report_text}
"""

                    response = llm.invoke(prompt)

                else:

                    prompt = f"""
Analyze this uploaded medical report image.

The report may be:

- Blood Report
- CBC Report
- Thyroid Report
- Kidney Report
- Liver Report
- Urine Report
- MRI Report
- CT Scan Report
- X-Ray Report
- Discharge Summary
- Prescription

Provide:

# 📊 Health Risk Dashboard

🔴 High Risk Findings

🟠 Moderate Risk Findings

🟢 Normal Findings

# 🩺 Patient-Friendly Summary

# ⚠️ Abnormal Findings

# 🧪 Test Results Breakdown

For each parameter include:

- Value
- Normal Range
- Risk Level
- Explanation

# 🌐 Explanation Language

Provide explanation in {language}

# 👨‍⚕️ Questions To Ask Doctor

Generate 5 questions.

# 📋 Health Recommendations
"""

                    response = llm.invoke(prompt)

                st.success("✅ Analysis Complete")

                st.markdown(response.content)

                st.download_button(
                    t["download"],
                    response.content,
                    file_name="medical_report_analysis.md",
                    mime="text/markdown"
                )

            except Exception as e:

                st.error(f"AI Error: {e}")

# ---------------------------------------------------
# DISCLAIMER
# ---------------------------------------------------

st.warning(
    f"""
{t["disclaimer_title"]}

{t["disclaimer"]}
"""
)