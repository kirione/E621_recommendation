import streamlit as st
import time

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'started' not in st.session_state:
    st.session_state.started = False

# Base styling with snow background
st.markdown("""
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
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
      background-color: #1f3b66 !important;
    }
    
    [data-testid="stSidebar"] * {
      color: white !important;
    }
    
    /* Top bar */
    [data-testid="stHeader"] {
      background-color: #021024 !important;
    }
    
    h1, h2, h3, p {
        color: white !important;
        text-align: center;
    }
    

    /* start scene css */
    .startscene_roll-container {
    font-size: 120px;
    font-weight: 800;
    text-align: center;
    perspective: 2000px;
    margin-top: 80px;
    }
            
    #roll-text .char {
    display: inline-block;
    color: white;              /* uses parent's color */
    transform-origin: center center -120px;
    text-shadow: 0 0 15px rgba(255,255,255,0.6);
    }

    .big-text {
        font-size: 80px;
        font-weight: bold;
        text-align: center;
        color: white !important;
        animation: fadeInUp 1s ease-out;
    }
    
    .stat-text {
        font-size: 120px;
        font-weight: bold;
        text-align: center;
        color: #FFD700 !important;
        animation: scaleIn 0.8s ease-out;
    }
    
    .description {
        font-size: 24px;
        text-align: center;
        color: white !important;
        animation: fadeIn 1s ease-out 0.5s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.5);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Primary, direct button selectors */
    div[data-testid="stButton"] > button,
    button[data-testid="stButton"],
    button[role="button"],
    button[class*="css-"],
    div[data-baseweb="button"] > button,
    [data-baseweb="button"] button,
    .stButton > button,
    button.stButton {
        background-image: none !important;
        background-color: black !important;   /* DEFAULT color: gold - change as you like */
        color: white !important;
        font-size: 20px !important;
        padding: 15px 40px !important;
        border-radius: 30px !important;
        font-weight: 700 !important;
        transition: transform 1s ease;
    }

    /* Hover / focus / active (make hover slightly darker) */
    div[data-testid="stButton"] > button:hover,
    button[role="button"]:hover,
    button[class*="css-"]:hover,
    div[data-baseweb="button"] > button:hover,
    .stButton > button:hover {
        background-color: black !important; /* darker gold on hover */
        color: white !important;
        transform: scale3d(1.3, 1.3, 1) !important;
    }

    
    </style>
    
    <div id="bg"></div>
    <div id="snow-container"></div>
""", unsafe_allow_html=True)

# GSAP animations for snow and stats
st.components.v1.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/split-type"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    </head>
    <body>
        <script>
            function animateElements() {
                const parentDoc = window.parent.document;
                
                // Find elements and add extra GSAP animations
                const stats = parentDoc.querySelectorAll('.stat-text');
                stats.forEach((stat, i) => {
                    if (typeof gsap !== 'undefined') {
                        gsap.from(stat, {
                            scale: 0.5,
                            rotation: -180,
                            duration: 1,
                            ease: "back.out(1.7)",
                            delay: i * 0.2
                        });
                    }
                });
            }
            
            // Run periodically to catch new elements
            setInterval(animateElements, 100);
            
            // Snow animation
            function initSnow() {
              if (typeof gsap === 'undefined') {
                setTimeout(initSnow, 100);
                return;
              }
              
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
            // start scene text animation
            document.addEventListener("DOMContentLoaded", function () {

                const parentDoc = window.parent.document;

                const rollText = parentDoc.querySelector('#roll-text');
                if (!rollText) return;

                const text = new SplitType(rollText, { types: 'chars' });

                // animate characters
                gsap.set(parentDoc.querySelectorAll('.char'), {
                    transformStyle: "preserve-3d",
                    rotationX: -90,
                    opacity: 0
                });

                gsap.to(parentDoc.querySelectorAll('.char'), {
                    rotationX: 270,
                    opacity: 1,
                    duration: 3,
                    ease: "none",
                    stagger: {
                        each: 0.06,
                        repeat: -1,
                        repeatDelay: 0.3
                    }
                });

            });
        </script>
    </body>
    </html>
""", height=0)

# Helper function to advance step
def next_step():
    st.session_state.step += 1
    time.sleep(0.1)  # Small delay for state update

def start_experience():
    st.session_state.started = True
    st.session_state.step = 1

# START SCREEN
if not st.session_state.started:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div id="roll-text" class="startscene_roll-container">E621 Wrapped 2025</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Let's Go!", use_container_width=True):
            start_experience()
            st.rerun()

# STEP 1: Top Tag
elif st.session_state.step == 1:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="big-text">Your Top Tag</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="stat-text">furry</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="description">You viewed this tag 1,247 times</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next", use_container_width=True, key="next1"):
            next_step()
            st.rerun()

# STEP 2: Total Views
elif st.session_state.step == 2:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="big-text">You Viewed</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="stat-text">5,842</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="description">posts this year</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next", use_container_width=True, key="next2"):
            next_step()
            st.rerun()

# STEP 3: Top 3 Tags
elif st.session_state.step == 3:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="big-text">Your Top 3 Tags</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-text">1</div>', unsafe_allow_html=True)
        st.markdown('<div class="description">furry</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-text">2</div>', unsafe_allow_html=True)
        st.markdown('<div class="description">anthro</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-text">3</div>', unsafe_allow_html=True)
        st.markdown('<div class="description">dragon</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next", use_container_width=True, key="next3"):
            next_step()
            st.rerun()

# STEP 4: Final Screen
elif st.session_state.step == 4:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="big-text">🎉 That\'s Your Wrap! 🎉</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="description">Thanks for an amazing year!</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start Over", use_container_width=True):
            st.session_state.step = 0
            st.session_state.started = False
            st.rerun()