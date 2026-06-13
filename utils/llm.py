import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(api_key):

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )