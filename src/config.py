import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if not GROQ_API_KEY:
        try:
            GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
        except Exception:
            GROQ_API_KEY = None

    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not GROQ_MODEL:
        try:
            GROQ_MODEL = st.secrets["GROQ_MODEL"]
        except Exception:
            GROQ_MODEL = "llama-3.3-70b-versatile"

    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing.")