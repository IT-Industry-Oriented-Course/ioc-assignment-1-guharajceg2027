"""Simple test UI to verify Streamlit works"""
import streamlit as st

st.set_page_config(page_title="Test UI", page_icon="🏥")

st.title("🏥 Clinical Workflow Automation Agent")
st.success("✅ Streamlit is working!")

st.write("If you can see this, Streamlit is running correctly.")
st.write("Now try running `streamlit run app.py` to see the full UI.")

