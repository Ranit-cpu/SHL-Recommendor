import streamlit as st
import requests

st.title("🔍 SHL Assessment Recommender")

query = st.text_area("Enter job description or natural language query:")
url = st.text_input("Or paste a job URL:")

if st.button("Recommend"):
    if not query and not url:
        st.warning("Please enter a query or a URL.")
    else:
        try:
            res = requests.post("http://localhost:8000/recommend", json={"query": query, "url": url})
            data = res.json()
            if res.status_code == 200 and isinstance(data, list) and data:
                st.write("### Recommended SHL Assessments")
                for item in data:
                    st.markdown(f"""
                    **[{item['name']}]({item['url']})**
                    - **Test Type**: {item.get('test_type', 'N/A')}
                    - **Duration**: {item.get('duration', 'N/A')}
                    - **Remote Testing Support**: {item.get('remote', 'N/A')}
                    - **Adaptive/IRT Support**: {item.get('adaptive', 'N/A')}
                    """)
            else:
                st.warning("No recommendations found or an error occurred.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Backend is not running.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
