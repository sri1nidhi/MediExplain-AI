import streamlit as st

from utils.pdf_loader import extract_pdf_text
from utils.llm import get_llm



st.set_page_config(
    page_title="MediExplain AI",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 MediExplain AI")
st.subheader("Understand Medical Reports in Simple Language")

uploaded_file = st.file_uploader(
    "Upload Medical Report PDF",
    type=["pdf"]
)

if uploaded_file:

    report_text = extract_pdf_text(uploaded_file)

    st.success("PDF Uploaded Successfully")

    if st.button("Analyze Report"):

        with st.spinner("Analyzing Report..."):

            llm = get_llm()

            prompt = f"""
               You are a medical report assistant.

               Analyze this report and provide:

               ## Simple Summary

               ## Important Findings

               ## Telugu Explanation

               ## Questions To Ask Doctor

               Medical Report:

               {report_text}
                """

            try:
                response = llm.invoke(prompt)

                st.success("Analysis Complete")

                st.markdown(response.content)
                st.download_button(
                    "📥 Download Summary",
                    response.content,
                    file_name="medical_report_summary.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"AI Error: {e}")

st.warning(
    "This tool is for educational purposes only."
)