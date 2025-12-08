import streamlit as st
import pandas as pd
import json
from targetsample_taginterest_analysis import tag_analysis

# -------------------------------
# ✅ PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="E621 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# ✅ INJECT CSS & BACKGROUND HTML
# -------------------------------
st.markdown(
    """
    <style>
    
    #bg {
      position: fixed;
      inset: 0;
      background: linear-gradient(to bottom, #021024, #1f3b66);
      z-index: -999;
      pointer-events: none;
    }

    #snow-container {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: -998;
      overflow: hidden;
    }

    .snowflake {
      position: absolute;
      top: -20px;
      color: white;
      font-size: 20px;
      user-select: none;
      pointer-events: none;
    }

    .stApp {
      background: transparent !important;

    }

    .stApp > header {
      background: transparent !important;
    }

    
    h1, h2, h3, h4, h5, h6 {
      color: white !important;
    }
    
    p, span, div, label {
      color: white !important;
    }

    /* Force selectbox text to be black */
    [data-baseweb="select"] {
      color: black !important;
    }
    
    [data-baseweb="select"] > div {
      color: black !important;
    }
    
    [data-baseweb="select"] input {
      color: black !important;
    }
    
    [data-baseweb="select"] span {
      color: black !important;
    }
    
    .stSelectbox select {
      color: black !important;
    }
    
    .stSelectbox div[data-baseweb="select"] div {
      color: black !important;
    }

    /* Dropdown menu options */
    [data-baseweb="popover"] {
      color: black !important;
    }
    
    [data-baseweb="popover"] li {
      color: black !important;
    }
    
    [data-baseweb="popover"] div {
      color: black !important;
    }
    
    [role="option"] {
      color: black !important;
    }
    
    [role="listbox"] li {
      color: black !important;
    }

    </style>
    
    <div id="bg"></div>
    <div id="snow-container"></div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# ✅ INJECT GSAP & JAVASCRIPT (Must be separate)
# -------------------------------
st.components.v1.html(
    """
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    </head>
    <body>
      <script>
        const setSelectboxColor = () => {
          const parentDoc = window.parent.document;
          
          // Target all selectbox elements in parent document
          const selectboxes = parentDoc.querySelectorAll("select, div[data-baseweb='select'] input");
          selectboxes.forEach(s => {
            s.style.color = "black";
            s.style.backgroundColor = "white";
          });
          
          // Also target the select container
          const selectContainers = parentDoc.querySelectorAll("div[data-baseweb='select']");
          selectContainers.forEach(c => {
            c.style.color = "black";
          });
        };

        // Run after page loads and periodically to catch new selectboxes
        setInterval(setSelectboxColor, 100);

      
        function initSnow() {
          if (typeof gsap === 'undefined') {
            setTimeout(initSnow, 100);
            return;
          }
          
          // Access parent document
          const parentDoc = window.parent.document;
          const snowContainer = parentDoc.getElementById("snow-container");
          
          if (!snowContainer) {
            setTimeout(initSnow, 100);
            return;
          }

          // Clear existing snowflakes
          snowContainer.innerHTML = '';

          // Create 80 snowflakes
          for (let i = 0; i < 80; i++) {
            const flake = parentDoc.createElement("div");
            flake.className = "snowflake";
            flake.textContent = "❄";

            const startX = Math.random() * parentDoc.documentElement.clientWidth;
            const size = Math.random() * 15 + 10;

            flake.style.left = startX + "px";
            flake.style.fontSize = size + "px";
            flake.style.opacity = Math.random() * 0.6 + 0.4;

            snowContainer.appendChild(flake);

            gsap.to(flake, {
              y: parentDoc.documentElement.clientHeight + 40,
              x: "+=" + (Math.random() * 100 - 50),
              rotation: Math.random() * 360,
              duration: Math.random() * 5 + 6,
              delay: Math.random() * 5,
              repeat: -1,
              ease: "none",
              onRepeat: function() {
                gsap.set(flake, {
                  y: -20,
                  x: Math.random() * parentDoc.documentElement.clientWidth,
                  rotation: 0
                });
              }
            });
          }
        }
        
        initSnow();
      </script>
    </body>
    </html>
    """,
    height=0,
    scrolling=False
)

# -------------------------------
# ✅ LOAD DATA
# -------------------------------
users_taginterest_df = pd.read_json(
    "E621_data/users_taginterest.json",
    lines=True
)

with open("E621_data/globalaverage_taginterest.json", "r", encoding="utf-8") as f:
    globalaverage_taginterest_data = json.load(f)

globalaverage_taginterest_df = pd.DataFrame(
    list(globalaverage_taginterest_data.items()),
    columns=["tag", "global_average"]
)

# -------------------------------
# ✅ STREAMLIT UI
# -------------------------------
st.title("❄️ E621 GSAP Dashboard")

st.subheader("📊 E621 Tags")

target_tag = st.selectbox(
    "Select An E621 Tag to analyse",
    options=globalaverage_taginterest_df["tag"].tolist()
)

st.subheader(
    f"Top 10 Tags Enjoyed by Users Who Like {target_tag}"
)

target_tag_enjoyment = tag_analysis(target_tag)

target_tag_enjoyment_series = (
    pd.Series(target_tag_enjoyment)
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(target_tag_enjoyment_series)

st.image(
    "https://static1.e621.net/data/sample/b1/87/b187e41db4063a0bd9934c643835751f.jpg",
    width=400
)