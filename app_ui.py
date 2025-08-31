import streamlit as st
from app import explain_bug

st.title("🐞 AI Bug Explainer")

error_message = st.text_input("Know About Your Bug")
if st.button("Explain"):
    result = explain_bug(error_message)
    st.write(result)
