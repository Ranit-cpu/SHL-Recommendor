import streamlit as st
import requests

st.title("🔍 SHL Assessment Recommender")
query = st.text_input("Enter job description or natural language query:")
url = st.text_input("Or paste a job URL:")

if st.button("Recommend"):
    try:
        res = requests.post("http://localhost:8000/recommend", json={"query": query, "url": url})
        st.write("Status Code:", res.status_code)
        st.write("Raw Response Text:", res.text)  # 👈 shows actual error message
        data = res.json()
        if data:
            st.write("### Recommended SHL Assessments")
            st.table(data)
        else:
            st.warning("No recommendations found.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Backend not running.")
    except requests.exceptions.JSONDecodeError:
        st.error("❌ Couldn't decode JSON from the backend. Check the backend logs.")
