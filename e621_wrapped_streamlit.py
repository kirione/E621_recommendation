import streamlit as st

st.set_page_config(
    page_title="E621 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

pg = st.navigation([
    st.Page("dashboard.py", title="🏠 Dashboard"),
    st.Page("wrapped_example.py", title="🎉 2025 Wrapped")
])
pg.run()
