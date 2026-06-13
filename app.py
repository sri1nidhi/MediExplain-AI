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
# HEADER
# ---------------------------------------------------

st.title("🩺 MediExplain AI")
st.subheader(
    "Understand Medical Reports in Simple Language"
)

# ---------------------------------------------------
# LANGUAGE
# ---------------------------------------------------

language = st.selectbox(
    "🌐 Choose Language",
    [
        "English",
        "Telugu",
        "Hindi"
    ]
)

# ---------------------------------------------------
# API KEY
# ---------------------------------------------------

api_key = st.text_input(
    "🔑 Enter Gemini API Key",
    type="password"
)

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload Medical Report",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg"
    ]
)

# ---------------------------------------------------
# PROCESS FILE
# ---------------------------------------------------

if uploaded_file:

    st.success("✅ Report Uploaded Successfully")

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
        st.warning(
            "Please enter Gemini API Key"
        )
        st.stop()

    if st.button("🔍 Analyze Report"):

        with st.spinner("Analyzing Report..."):

            llm = get_llm(api_key)

            try:

                # ----------------------------------
                # PDF ANALYSIS
                # ----------------------------------

                if is_pdf:

                    prompt = f"""
You are an expert medical report analyzer.

Analyze this hospital report.

The report can be:

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

For every test include:

- Value
- Normal Range
- Risk Level
- Explanation

# 🌐 Language

Explain in {language}

# 👨‍⚕️ Questions To Ask Doctor

Generate 5 questions.

# 📋 Recommendations

Medical Report:

{report_text}
"""

                    response = llm.invoke(prompt)

                # ----------------------------------
                # IMAGE ANALYSIS
                # ----------------------------------

                else:

                    response = llm.invoke(
                        f"""
Analyze the uploaded medical report image.

Provide:

# 📊 Health Risk Dashboard

🔴 High Risk Findings

🟠 Moderate Risk Findings

🟢 Normal Findings

# 🩺 Patient-Friendly Summary

# ⚠️ Abnormal Findings

# 🧪 Test Results Breakdown

# 🌐 Explain in {language}

# 👨‍⚕️ Questions To Ask Doctor

# 📋 Recommendations
"""
                    )

                st.success("✅ Analysis Complete")

                st.markdown(response.content)

                st.download_button(
                    "📥 Download Analysis",
                    response.content,
                    file_name="medical_report_analysis.md",
                    mime="text/markdown"
                )

            except Exception as e:

                st.error(
                    f"AI Error: {e}"
                )

# ---------------------------------------------------
# DISCLAIMER
# ---------------------------------------------------

st.warning(
    """
⚠️ Disclaimer

This tool is for educational purposes only.

The generated analysis is NOT a medical diagnosis.

Please consult a qualified healthcare professional before making medical decisions.
"""
)