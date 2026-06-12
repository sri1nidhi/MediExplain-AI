import streamlit as st

from utils.pdf_loader import extract_pdf_text
from utils.image_loader import extract_image_text
from utils.llm import get_llm

# -----------------------
# Page Config
# -----------------------

st.set_page_config(
    page_title="MediExplain AI",
    page_icon="🩺",
    layout="wide"
)

# -----------------------
# Language Text
# -----------------------

TEXT = {
    "English": {
        "title": "🩺 MediExplain AI",
        "subtitle": "Understand Medical Reports in Simple Language",
        "upload": "📄 Upload Medical Report",
        "analyze": "🔍 Analyze Report",
        "apikey": "🔑 Enter Gemini API Key"
    },
    "Telugu": {
        "title": "🩺 మెడి ఎక్స్‌ప్లైన్ AI",
        "subtitle": "మెడికల్ రిపోర్టులను సులభంగా అర్థం చేసుకోండి",
        "upload": "📄 మెడికల్ రిపోర్ట్ అప్లోడ్ చేయండి",
        "analyze": "🔍 రిపోర్ట్ విశ్లేషించండి",
        "apikey": "🔑 Gemini API Key నమోదు చేయండి"
    },
    "Hindi": {
        "title": "🩺 मेडीएक्सप्लेन AI",
        "subtitle": "मेडिकल रिपोर्ट को आसान भाषा में समझें",
        "upload": "📄 मेडिकल रिपोर्ट अपलोड करें",
        "analyze": "🔍 रिपोर्ट का विश्लेषण करें",
        "apikey": "🔑 Gemini API Key दर्ज करें"
    }
}

# -----------------------
# Header
# -----------------------

language = st.selectbox(
    "🌐 Language",
    ["English", "Telugu", "Hindi"]
)

st.title(TEXT[language]["title"])
st.subheader(TEXT[language]["subtitle"])

# -----------------------
# API Key
# -----------------------

api_key = st.text_input(
    TEXT[language]["apikey"],
    type="password"
)

# -----------------------
# Upload
# -----------------------

uploaded_file = st.file_uploader(
    TEXT[language]["upload"],
    type=["pdf", "png", "jpg", "jpeg"]
)

# -----------------------
# Processing
# -----------------------

if uploaded_file:

    try:

        if uploaded_file.type == "application/pdf":
            report_text = extract_pdf_text(uploaded_file)

        else:

            st.image(
                uploaded_file,
                caption="Uploaded Report",
                use_container_width=True
            )

            report_text = extract_image_text(uploaded_file)

        st.success("✅ Report Uploaded Successfully")

        if st.button(TEXT[language]["analyze"]):

            if not api_key:
                st.warning("⚠️ Please enter Gemini API Key")
                st.stop()

            with st.spinner("Analyzing Report..."):

                llm = get_llm(api_key)

                prompt = f"""
You are an expert medical report analyzer.

Analyze any medical report.

Supported Reports:

- Blood Reports
- CBC Reports
- Thyroid Reports
- Kidney Reports
- Liver Reports
- Urine Reports
- MRI Reports
- CT Scan Reports
- X-Ray Reports
- Ultrasound Reports
- Discharge Summaries
- Prescription Documents

Return ONLY markdown.

# 📋 Report Type

Identify the report type.

# 📊 Health Risk Dashboard

Provide:

🔴 High Risk Findings

🟠 Moderate Risk Findings

🟢 Normal Findings

# 🩺 Patient-Friendly Summary

Explain the report in simple language.

# ⚠️ Abnormal Findings

List all abnormal values.

For each abnormal value explain:

- What it means
- Possible causes
- Severity

# 🧪 Test Results Breakdown

Create separate sections.

For every test include:

- Test Name
- Value
- Normal Range
- Risk Level
- Explanation

# 🌐 Explanation Language

Provide explanation in:

{language}

# 👨‍⚕️ Questions To Ask Doctor

Generate 5 useful questions.

# 📋 Health Recommendations

Provide general recommendations.

# ⚠️ Important Note

Mention that this is not a medical diagnosis.

Medical Report:

{report_text}
"""

                response = llm.invoke(prompt)

                st.success("✅ Analysis Complete")

                # Dashboard Section
                st.markdown("---")
                st.subheader("📊 Health Dashboard")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.error("🔴 High Risk Findings")

                with col2:
                    st.warning("🟠 Moderate Risk Findings")

                with col3:
                    st.success("🟢 Normal Findings")

                st.markdown("---")

                # AI Analysis
                st.markdown(response.content)

                # Download
                st.download_button(
                    "📥 Download Analysis",
                    response.content,
                    file_name=f"medical_analysis_{language}.md",
                    mime="text/markdown"
                )

    except Exception as e:
        st.error(f"Error: {e}")

# -----------------------
# Disclaimer
# -----------------------

st.warning(
    """
⚠️ Disclaimer


This tool is for educational purposes only.

The generated analysis is NOT a medical diagnosis.

Always consult a licensed healthcare professional before making any medical decisions.
"""
)