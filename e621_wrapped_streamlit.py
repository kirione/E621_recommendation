import streamlit as st
import pandas as pd
import numpy as np
import json as json
from targetsample_taginterest_analysis import tag_analysis
#Set page config
st.set_page_config(
    page_title="E621 Dashboard",
    layout="wide",  # <-- makes the page take full browser width
    initial_sidebar_state="expanded"
)
#Read json
users_taginterest_df = pd.read_json('E621_data/users_taginterest.json', lines=True)


with open('E621_data/globalaverage_taginterest.json', 'r', encoding='utf-8') as f:
    globalaverage_taginterest_data = json.load(f)


# Convert dict → row-wise DataFrame
globalaverage_taginterest_df = pd.DataFrame(
    list(globalaverage_taginterest_data.items()),
    columns=['tag', 'global_average']
)

#Layout
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("📊 E621 Tags")
    
    target_tag = st.selectbox("Select An E621 Tag to analyse", options=globalaverage_taginterest_df["tag"].tolist())

    #Top 10 tags associated with selected tag
    st.subheader(f"Top 10 Tags Enjoyed by Users Who Like {target_tag} (In enjoyment score - harmonic mean of tag frequency and relative to global average)")
    target_tag_enjoyment = tag_analysis(target_tag)
    target_tag_enjoyment_series = pd.Series(target_tag_enjoyment).sort_values(ascending=False).head(10)
    st.bar_chart(target_tag_enjoyment_series)


    st.image(
        "https://static1.e621.net/data/sample/b1/87/b187e41db4063a0bd9934c643835751f.jpg",
        width=400
    )

# -----------------------------
# RIGHT SIDE: Controls Panel
# -----------------------------
with col2:
    st.subheader("🎛 Controls Panel")

    date = st.date_input("Select Date")

    show_raw = st.checkbox("Show Raw Data")

    refresh = st.button("Refresh Data")

    if refresh:
        st.success("Data refreshed!")
    if show_raw:
        st.dataframe(globalaverage_taginterest_df)