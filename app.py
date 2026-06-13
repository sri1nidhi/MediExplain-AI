import streamlit as st
from PIL import Image

from utils.pdf_loader import extract_pdf_text
from utils.llm import get_llm


st.set_page_config(
    page_title="MediExplain AI",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 MediExplain AI")
st.subheader(
    "Understand Medical Reports in Simple Language"
)

# ----------------------------
# Language Selection
# ----------------------------

language = st.selectbox(
    "🌐 Choose Language",
    [
        "English",
        "Telugu",
        "Hindi"
    ]
)

# ----------------------------
# API Key
# ----------------------------

api_key = st.text_input(
    "🔑 Enter Gemini API Key",
    type="password"
)

# ----------------------------
# Upload
# ----------------------------

uploaded_file = st.file_uploader(
    "📄 Upload Medical Report",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg"
    ]
)

# ----------------------------
# Report Processing
# ----------------------------

if uploaded_file:

    st.success("✅ Report Uploaded Successfully")

    if uploaded_file.type.startswith("image"):

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

        with st.spinner("Analyzing Medical Report..."):

            try:

                llm = get_llm(api_key)

                # ----------------------------------
                # PDF REPORT
                # ----------------------------------

                if uploaded_file.type == "application/pdf":

                    report_text = extract_pdf_text(
                        uploaded_file
                    )

                    prompt = f"""
You are an expert medical report analyzer.

Analyze this medical report.

Return ONLY markdown.

# 📊 Health Risk Dashboard

Show:

🔴 High Risk Findings

🟠 Moderate Risk Findings

🟢 Normal Findings

# 🩺 Patient-Friendly Summary

Explain in simple language.

# ⚠️ Abnormal Findings

List abnormal values.

# 🧪 Test Results Breakdown

For every parameter provide:

- Value
- Normal Range
- Risk Level
- Explanation

# 🌐 Language

Provide explanation in {language}.

# 👨‍⚕️ Questions To Ask Doctor

Generate 5 questions.

# 📋 Recommendations

Provide health recommendations.

Medical Report:

{report_text}
"""

                    response = llm.invoke(prompt)

                # ----------------------------------
                # IMAGE REPORT
                # ----------------------------------

                else:

                    image = Image.open(
                        uploaded_file
                    )

                    response = llm.invoke([
                        f"""
You are an expert medical report analyzer.

Analyze this medical report image.

The report may be:

- Blood Test
- CBC
- Thyroid
- MRI
- CT Scan
- X-Ray
- Urine Test
- Liver Function Test
- Kidney Function Test
- Prescription
- Discharge Summary

Return ONLY markdown.

# 📊 Health Risk Dashboard

Show:

🔴 High Risk Findings

🟠 Moderate Risk Findings

🟢 Normal Findings

# 🩺 Patient-Friendly Summary

Explain in simple language.

# ⚠️ Abnormal Findings

List abnormal findings.

# 🧪 Test Results Breakdown

For every parameter provide:

- Value
- Normal Range
- Risk Level
- Explanation

# 🌐 Language

Provide explanation in {language}.

# 👨‍⚕️ Questions To Ask Doctor

Generate 5 questions.

# 📋 Recommendations

Provide health recommendations.
""",
                        image
                    ])

                st.success(
                    "✅ Analysis Complete"
                )

                st.markdown(
                    response.content
                )

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

# ----------------------------
# Disclaimer
# ----------------------------

st.warning(
    """
⚠️ Disclaimer

This tool is for educational purposes only.

The generated analysis is NOT a medical diagnosis.

Please consult a licensed healthcare professional.
"""
)