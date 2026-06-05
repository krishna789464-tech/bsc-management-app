import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time
import base64
import streamlit.components.v1 as components
from PIL import Image

# Safely attempt to import Google's official Generative AI library
try:
    import google.generativeai as genai
    gemini_installed = True
except ImportError:
    gemini_installed = False

# --- 1. ACCESSIBILITY & BRIGHTNESS SESSION STATE ---
if "font_scale" not in st.session_state:
    st.session_state.font_scale = 100  # Default font percentage
if "bg_theme" not in st.session_state:
    st.session_state.bg_theme = "light"  # Default theme
if "animation_played" not in st.session_state:
    st.session_state.animation_played = False
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I am your Google Gemini-powered Academic Advisor. Paste your API key in the sidebar to run live queries, or test me using standard heuristics!"}
    ]

# --- 2. CINEMATIC STARTING ANIMATION ---
if not st.session_state.animation_played:
    animation_html = """
    <div id="animation-overlay">
        <div class="content-wrapper">
            <h1 class="welcome-text">HELLO STUDENTS</h1>
            <div class="sub-bar"></div>
            <p class="portal-text">Academic Student Portal</p>
        </div>
    </div>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap');
        #animation-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(135deg, #0b0f19 0%, #1e40af 50%, #020617 100%);
            display: flex; justify-content: center; align-items: center;
            z-index: 999999; font-family: 'Inter', sans-serif; overflow: hidden;
            animation: fadeOutWindow 1s cubic-bezier(0.7, 0, 0.3, 1) forwards;
            animation-delay: 3.5s;
        }
        .content-wrapper { text-align: center; display: flex; flex-direction: column; align-items: center; }
        .welcome-text {
            font-size: 4rem; font-weight: 800; letter-spacing: 6px; color: #ffffff; margin: 0; text-transform: uppercase;
            background: linear-gradient(to right, #ffffff, #93c5fd, #ffffff); background-size: 200% auto;
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shineText 3s linear infinite, scaleUpText 2.5s cubic-bezier(0.1, 0.8, 0.2, 1) forwards; opacity: 0;
        }
        .sub-bar {
            width: 0px; height: 4px; background: #3b82f6; margin-top: 15px; margin-bottom: 15px;
            box-shadow: 0px 0px 15px #3b82f6; animation: growBar 1.5s ease-out forwards; animation-delay: 0.8s;
        }
        .portal-text { font-size: 1.2rem; font-weight: 400; letter-spacing: 4px; color: #94a3b8; margin: 0; text-transform: uppercase; opacity: 0; animation: fadeInPortal 1.5s ease-out forwards; animation-delay: 1.5s; }
        @keyframes scaleUpText { 0% { transform: scale(0.85); opacity: 0; filter: blur(10px); } 30% { opacity: 1; filter: blur(0px); } 100% { transform: scale(1.05); opacity: 1; } }
        @keyframes shineText { to { background-position: 200% center; } }
        @keyframes growBar { to { width: 250px; } }
        @keyframes fadeInPortal { to { opacity: 1; } }
        @keyframes fadeOutWindow { to { opacity: 0; visibility: hidden; pointer-events: none; } }
    </style>
    """
    components.html(animation_html, height=0)
    time.sleep(4.2) 
    st.session_state.animation_played = True
    st.rerun()

# --- 3. CONFIGURATION & STYLING ---
LOGO_PATH = r"C:\Users\ADMIN\Desktop\app logo.png"
logo_exists = os.path.exists(LOGO_PATH)

if logo_exists:
    try:
        app_logo = Image.open(LOGO_PATH)
        page_icon_val = app_logo
    except Exception:
        app_logo = None
        page_icon_val = "🎓"
else:
    app_logo = None
    page_icon_val = "🎓"

st.set_page_config(
    page_title="Academic Student Portal",
    page_icon=page_icon_val,
    layout="wide"
)

# --- 4. LOCAL BACKGROUND IMAGE (BASE64 CONVERSION) ---
BG_IMAGE_PATH = r"C:\Users\ADMIN\Desktop\modern-light-blue-background-featuring-circuit-line-elements-and-dotted-texture-perfect-for-digital-technology-themes-presentations-web-interfaces-and-tech-branding-vector.jpg"

@st.cache_data
def get_base64_of_local_image(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

bg_base64 = get_base64_of_local_image(BG_IMAGE_PATH)

if st.session_state.bg_theme == "light":
    card_bg = "rgba(255, 255, 255, 0.88)"  
    text_color = "#0f172a"
    sub_text_color = "#475569"
    border_color = "#cbd5e1"
    tab_active_text = "#ffffff"
    overlay_tint = "rgba(241, 245, 249, 0.25)"  
else:
    card_bg = "rgba(15, 23, 42, 0.88)"   
    text_color = "#f8fafc"
    sub_text_color = "#94a3b8"
    border_color = "#2d3748"
    tab_active_text = "#ffffff"
    overlay_tint = "rgba(11, 15, 25, 0.65)"  

if bg_base64:
    background_style = f"""
    background: linear-gradient({overlay_tint}, {overlay_tint}), 
                url("data:image/jpeg;base64,{bg_base64}") no-repeat center center fixed;
    background-size: cover !important;
    """
else:
    background_style = f"background-color: {'#f1f5f9' if st.session_state.bg_theme == 'light' else '#0b0f19'} !important;"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: {st.session_state.font_scale}% !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        {background_style}
    }}
    
    h1 {{ font-size: 2rem !important; color: {text_color} !important; font-weight: 700 !important; }}
    h2 {{ font-size: 1.6rem !important; color: {text_color} !important; font-weight: 700 !important; }}
    h3 {{ font-size: 1.25rem !important; color: {text_color} !important; font-weight: 600 !important; }}
    h4 {{ font-size: 1.1rem !important; color: {text_color} !important; font-weight: 600 !important; }}
    p, span, label, li, td {{ color: {text_color} !important; }}
    
    [data-testid="stHeader"] {{ display: none !important; height: 0px !important; }}
    .block-container {{ padding-top: 1rem !important; padding-bottom: 2rem !important; }}
    
    .main-card {{ 
        padding: 20px; 
        border-radius: 12px; 
        background: {card_bg}; 
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); 
        border: 1px solid {border_color}; 
    }}
    
    .metric-card {{ 
        background: {card_bg} !important; 
        backdrop-filter: blur(10px);
        padding: 18px; 
        border-radius: 12px; 
        text-align: center; 
        border: 1px solid {border_color} !important; 
        margin-bottom: 12px; 
    }}
    
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {{ 
        gap: 6px; 
        background-color: {card_bg}; 
        backdrop-filter: blur(10px);
        padding: 6px; 
        border-radius: 12px; 
        border: 1px solid {border_color}; 
    }}
    
    div[data-testid="stTabs"] [data-baseweb="tab"] {{ padding: 6px 12px; border-radius: 8px; font-weight: 500; color: {sub_text_color} !important; }}
    div[data-testid="stTabs"] [aria-selected="true"] {{ background-color: #2563eb !important; color: {tab_active_text} !important; }}
    
    div[data-testid="stAppDeployButton"] {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; }}
    footer {{ visibility: hidden !important; }}
    .stForm {{ background: {card_bg} !important; backdrop-filter: blur(10px); border: 1px solid {border_color} !important; border-radius: 12px !important; padding: 20px !important; }}
    
    .highlight-box {{
        background: linear-gradient(135deg, rgba(37,99,235,0.1), rgba(37,99,235,0.05));
        border: 1px dashed #2563eb;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 10px;
        font-weight: 600;
        color: #2563eb !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR: GOOGLE GEMINI KEY & PROFILE MANAGER ---
with st.sidebar:
    st.markdown("### 🔑 Google Gemini Setup")
    gemini_key = st.text_input(
        "Gemini API Key", 
        type="password", 
        placeholder="Paste API Key (AIzaSy...)",
        help="Paste your Gemini key here to activate live AI generation."
    )
    
    st.markdown("[Get a free Gemini API Key 🔑](https://aistudio.google.com/)")
    
    # Verify and configure library live
    is_gemini_active = False
    if gemini_key:
        if gemini_installed:
            try:
                genai.configure(api_key=gemini_key.strip())
                is_gemini_active = True
                st.success("🟢 Connected to Google Gemini")
            except Exception as e:
                st.error(f"Configuration failed: {e}")
        else:
            st.warning("Please run: `pip install google-generativeai` to support live connection.")
    else:
        st.info("Currently in Standard (Heuristic) Sandbox mode.")
        
    st.markdown("---")
    st.markdown("### 👤 Student Profile")
    major_focus = st.selectbox("Academic Track", ["B.Sc Geology Group", "B.Sc Physics Group", "B.Sc Mathematics Group"])
    current_year = st.selectbox("Current Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI"])

# --- AI CORE QUERY TRANSCEIVER ---
def execute_academic_ai(prompt, context_system=""):
    """
    Executes an AI query. If Google Gemini is successfully set up and active, 
    it retrieves a live response using the 'gemini-1.5-flash' model. 
    Otherwise, it utilizes a local rule-based system.
    """
    if is_gemini_active:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            full_prompt = f"{context_system}\n\nStudent Request: {prompt}" if context_system else prompt
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"*(Gemini live generation errored: {e}. Defaulting to local sandbox answers)*"

    # Rule-Based Sandbox Fallbacks
    prompt_lower = prompt.lower()
    if "plan" in prompt_lower or "schedule" in prompt_lower or "calendar" in prompt_lower:
        return f"""
### 📅 Recommended Weekly Study Structure ({major_focus})
*(Sandbox Heuristic Profile)*
* **Day 1-2**: Focus on primary core subjects (e.g., Crystallography or Mechanics). Read 1 key paper/chapter.
* **Day 3-4**: Practical review. Work on mathematics assignments or diagram plotting.
* **Day 5**: Active recall session. Generate 5 self-assessment questions.
* **Weekend**: Cumulative review and problem solving. Solve past year Lucknow University papers.
        """
    elif "geology" in prompt_lower:
        return """
### 💎 Structural Geology & Mineral
