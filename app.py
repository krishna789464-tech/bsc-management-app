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
            # Using gemini-1.5-flash as the fast, efficient standard model
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
### 💎 Structural Geology & Mineralogy Insights
*(Sandbox Heuristic Profile)*
* **Structural Geology**: Focus on distinguishing between *Faults* (brittle deformation with displacement) and *Folds* (ductile deformation displaying structural wave curvature).
* **Mineralogy**: Master key optical mineral properties including *Pleochroism* under Plane Polarized Light and *Interference Colors* under Crossed Polars.
* **Recommended Resource**: Review physical hand specimens in the college laboratory.
        """
    elif "math" in prompt_lower or "calculus" in prompt_lower or "equation" in prompt_lower:
        return """
### 📐 Advanced Engineering Mathematics Blueprint
*(Sandbox Heuristic Profile)*
* **Ordinary Differential Equations**: Master Euler-Cauchy equations and the method of variation of parameters.
* **Linear Algebra**: Focus heavily on Eigenvalues, Eigenvectors, and satisfying the Cayley-Hamilton theorem.
* **Practice Strategy**: Dedicate 45 minutes daily to derivation structures rather than rote-learning proofs.
        """
    else:
        return f"""
### 🎓 Academic Support Response
*(Sandbox Heuristic Profile)*
Based on your academic profile ({major_focus} | {current_year}):
* We advise cross-referencing your syllabus with the recommended readings in **Tab 7 (Study Classrooms)**.
* To generate actual bespoke guidance, connect your free Gemini API Key in the sidebar.
* **Study Hint**: Prioritize clarifying practical diagrams first; conceptual understanding often follows structural visual mapping.
        """

# Running Clock Markup
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"
NOTEBOOK_LM_URL = "https://notebooklm.google.com/notebook/4865426e-ee8e-4256-956c-9f09f7c6c332?addSource=true"

clock_html = f"""
<div id="clock-container" style="font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: {text_color}; text-align: right; padding-right: 5px;">
    <span id="date-part"></span> &nbsp;&bull;&nbsp; <span id="time-part" style="color: #2563eb; font-weight: 700;"></span>
</div>
<script>
    function updateClock() {{
        const now = new Date();
        const options = {{ year: 'numeric', month: 'long', day: 'numeric' }};
        document.getElementById('date-part').textContent = "📅 " + now.toLocaleDateString('en-US', options);
        let hours = now.getHours(); const minutes = String(now.getMinutes()).padStart(2, '0'); const seconds = String(now.getSeconds()).padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM'; hours = hours % 12; hours = hours ? hours : 12;
        document.getElementById('time-part').textContent = "🕒 " + String(hours).padStart(2, '0') + ':' + minutes + ':' + seconds + ' ' + ampm;
    }}
    setInterval(updateClock, 1000); updateClock();
</script>
"""

# App Layout Header
header_col, control_col = st.columns([2.3, 1.3])
with header_col:
    st.markdown("<h2 style='margin: 0; color: #1e40af;'>🎓 Academic Student Portal</h2>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 0.9rem; opacity: 0.85;'>Verification Tier: B.Sc Undergraduate • Helpdesk: <a href='mailto:{ADMIN_EMAIL}' style='text-decoration:none; color:#2563eb; font-weight:500;'>{ADMIN_EMAIL}</a></span>", unsafe_allow_html=True)

with control_col:
    components.html(clock_html, height=32)
    suite_col1, suite_col2 = st.columns(2)
    with suite_col1:
        theme_idx = 0 if st.session_state.bg_theme == "light" else 1
        theme_choice = st.selectbox("Theme", ["☀️ Light", "🌙 Dark"], index=theme_idx, key="top_theme_select")
        selected_theme = "light" if "Light" in theme_choice else "dark"
        if selected_theme != st.session_state.bg_theme:
            st.session_state.bg_theme = selected_theme
            st.rerun()
    with suite_col2:
        font_idx = 0 if st.session_state.font_scale == 100 else (1 if st.session_state.font_scale == 120 else 2)
        font_choice = st.selectbox("Font Size", ["🔍 100%", "🔍 120%", "🔍 140%"], index=font_idx, key="top_font_select")
        selected_scale = 100 if "100%" in font_choice else (120 if "120%" in font_choice else 140)
        if selected_scale != st.session_state.font_scale:
            st.session_state.font_scale = selected_scale
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
st.warning("⚠️ **System Notice / आवश्यक सूचना:** This portal is currently in the **testing phase**. (यह एप्लिकेशऩ अभी टेस्टिंग फेज़ में है।)")

# --- NAVIGATION TABS ---
tabs = st.tabs([
    "📊 Dashboard",
    "🏫 College Info Hub",  
    "🤖 Interactive AI Chatbot",
    "📚 AI Study Planner & Flashcards",
    "🔍 Deep Search (NotebookLM)",
    "📢 News & Notices",
    "📚 Study Classrooms",
    "🧮 Performance Toolkit",
    "⏱️ Focus Engine",
    "🚨 Report Issue"
])
(
    tab_dashboard, 
    tab_college, 
    tab_ai, 
    tab_planner, 
    tab_deep_search, 
    tab_news, 
    tab_study, 
    tab_perf, 
    tab_focus, 
    tab_report
) = tabs

# --- TAB: DASHBOARD ---
with tab_dashboard:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); color: white !important; padding: 24px; border-radius: 16px; margin-bottom: 24px; margin-top: 10px;">
            <h1 style="margin: 0; color: white !important; font-size:26px;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.95; margin-top: 8px; font-size: 14px; max-width: 700px; color: white !important;">
                Central administrative hub optimized for real-time classroom updates, digital asset access, performance management, and direct administrative escalation pathways.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1: st.markdown('<div class="metric-card"><h4>Total Cohort</h4><h2 style="color: #2563eb !important; margin:4px 0 0 0; font-size:24px;">1,250</h2></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="metric-card"><h4>Active Courses</h4><h2 style="color: #16a34a !important; margin:4px 0 0 0; font-size:24px;">18</h2></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="metric-card"><h4>Active Notices</h4><h2 style="color: #ea580c !important; margin:4px 0 0 0; font-size:24px;">6</h2></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="metric-card"><h4>Pending Inquiries</h4><h2 style="color: #dc2626 !important; margin:4px 0 0 0; font-size:24px;">12</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.subheader("💡 Dynamic AI Study Briefing")
        brief_prompt = f"Provide a brief, high-level structural study recommendation for a {major_focus} student starting {current_year} semester. Keep it under 3 bullets."
        briefing = execute_academic_ai(brief_prompt)
        st.markdown(briefing)
        
        st.subheader("📚 Course Registration Status")
        materials = [
            {"subject": "Structural Geology", "teacher": "Dr. Sharma"},
            {"subject": "Mineralogy", "teacher": "Prof. Singh"},
            {"subject": "Engineering Mathematics", "teacher": "Dr. Verma"}
        ]
        for item in materials:
            with st.container():
                st.markdown(f"**{item['subject']}** — Instructor: {item['teacher']}")
                st.caption("🟢 Automated Sync Environment Active")
                st.divider()
                
    with right_col:
        st.subheader("⚡ Core Modules")
        st.button("📋 Live Attendance Tracker", use_container_width=True)
        st.button("📝 Assignment Log", use_container_width=True)
        st.button("📅 Academic Calendar", use_container_width=True)
        st.button("📊 Examination Reports", use_container_width=True)

# --- TAB: COLLEGE INFO HUB ---
with tab_college:
    st.header("🏫 College Information & ERP Gateway")
    st.write("Direct pipelines to campus notice desks, unified ledger lookups, and academic fee clearance terminals.")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown(f"""
            <div style="border: 1px solid {border_color}; background-color: {card_bg}; padding: 24px; border-radius: 12px; min-height: 270px; backdrop-filter: blur(8px);">
                <h3 style="margin-top:0; color:#2563eb;">💳 Transactions & Fee Clearance</h3>
                <p style="font-size:0.95rem; line-height:1.6;">
                    Track ledger adjustments or execute runtime registration charges. 
                    Access the external cloud terminals below to verify current financial clearings or clear backlogs.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("💳 Go to Transaction Search Terminal", "https://erpweb.bsnvpgcollege.co.in/transaction-search", type="secondary", use_container_width=True)
        st.link_button("💵 Process & Pay Course Fees Online", "https://erpweb.bsnvpgcollege.co.in/paycoursefees", type="primary", use_container_width=True)

    with col_right:
        st.markdown(f"""
            <div style="border: 1px solid {border_color}; background-color: {card_bg}; padding: 24px; border-radius: 12px; min-height: 270px; backdrop-filter: blur(8px); margin-bottom:15px;">
                <h3 style="margin-top:0; color:#ea580c;">📋 Institutional Notice Dashboard</h3>
                <p style="font-size:0.95rem; line-height:1.6;">
                    Access formal administrative directives, mid-term evaluation plans, and departmental announcements directly via the college's public communication network stack.
                </p>
                <span style="font-size:0.85rem; background-color:#ffedd5; color:#c2410c; padding:6px 12px; border-radius:6px; font-weight:600; display:inline-block; margin-top:10px;">
                    📢 Verified Structural Pipeline
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        st.link_button("📢 Launch Official Notice Board Terminal", "https://bsnvpgcollege.ac.in/NoticeHome.aspx?Type=Notice", type="primary", use_container_width=True)

# --- TAB: AI ASSISTANT ---

with tab_ai:

    st.header("🤖 AI Agent")

    st.write("Our automated academic agent is loading below. If it does not open automatically, look for the chat container asset.")

    jotform_script = "<script src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'></script>"

    components.html(jotform_script, height=550, scrolling=True)



# --- TAB: AI PLANNER & FLASHCARDS ---
with tab_planner:
    st.header("📚 Study Material & Flashcard Synthesizer")
    st.write("Generate interactive structural summaries, mock assessment questionnaires, or flashcard lists directly from a core topic.")
    
    col_p1, col_p2 = st.columns([1, 1])
    
    with col_p1:
        st.subheader("🛠️ Study Material Engine")
        syllabus_topic = st.text_input(
            "Syllabus Topic Name",
            placeholder="e.g., Optical Properties of Uniaxial Minerals under Polarizing Microscope",
            key="p_topic_input"
        )
        generation_type = st.radio(
            "Synthesis Goal",
            ["Summarized Study Guide", "5 Question Assessment Practice Quiz", "Interactive Conceptual Analogies"]
        )
        
        if st.button("Generate Learning Asset", type="primary", use_container_width=True):
            if syllabus_topic:
                system_prompt = f"Act as an educational material developer. The user is on the {major_focus} track. Provide highly structured output."
                user_prompt = f"Create a '{generation_type}' for the academic topic: '{syllabus_topic}'."
                with st.spinner("Synthesizing concept trees..."):
                    learning_output = execute_academic_ai(user_prompt, system_prompt)
                    st.markdown("---")
                    st.markdown(learning_output)
            else:
                st.error("Please enter a syllabus topic to trigger synthesis.")
                
    with col_p2:
        st.subheader("🃏 Interactive Flashcard Generator")
        flash_topic = st.text_input("Enter Topic for Flashcards", placeholder="e.g., Plate Tectonics Boundaries")
        
        if st.button("Generate Digital Flashcards", type="secondary", use_container_width=True):
            if flash_topic:
                system_prompt = "Act as an academic flashcard developer. Output exactly 3 clear Flashcards. Format each card clearly as: **CARD [Number]: Front (Term/Concept)** followed by a collapsible `with st.expander('Reveal Answer')` style text block or plain text answer block."
                user_prompt = f"Generate 3 flashcards for: '{flash_topic}'."
                with st.spinner("Processing cards..."):
                    flash_output = execute_academic_ai(user_prompt, system_prompt)
                    st.markdown("---")
                    st.markdown(flash_output)
            else:
                st.error("Please specify a topic to generate flashcards.")

# --- TAB: STREAMLINED DEEP SEARCH & VIDEO TERMINAL ---
with tab_deep_search:
    st.header("🔍 Deep Search & Multimedia Research")
    st.write("Direct external bridge pipelines to your academic analysis and video lecture workspaces.")
    
    search_col1, search_col2 = st.columns(2)
    
    with search_col1:
        st.markdown(f"""
            <div style="border: 1px solid {border_color}; background-color: {card_bg}; padding: 24px; border-radius: 12px; height: 260px; backdrop-filter: blur(8px);">
                <h3 style="margin-top:0; color:#2563eb;">Google NotebookLM Gateway</h3>
                <p style="font-size:0.95rem; line-height:1.6; margin-bottom: 20px;">
                    Clicking the link below establishes an external session handshake directly into your configured NotebookLM cluster. 
                    Manage documentation parsing, contextual index creation, and text automation routines.
                </p>
                <span style="font-size:0.85rem; background-color:#dcfce7; color:#15803d; padding:6px 12px; border-radius:6px; font-weight:600;">
                    🔗 Connection Pipeline Ready
                </span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.link_button(
            "🚀 Launch Connected NotebookLM Chat Session", 
            NOTEBOOK_LM_URL, 
            type="primary", 
            use_container_width=True
        )

    with search_col2:
        st.markdown(f"""
            <div style="border: 1px solid {border_color}; background-color: {card_bg}; padding: 24px; border-radius: 12px; height: 260px; backdrop-filter: blur(8px); margin-bottom: 0px;">
                <h3 style="margin-top:0; color:#ff0000;">YouTube Video Lecture Terminal</h3>
                <p style="font-size:0.95rem; line-height:1.6;">
                    Type your research topic, complex formula, or specific syllabus chapter below. 
                    The portal will sync the data string and launch YouTube directly with your filtered educational feed.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        yt_query = st.text_input(
            "Search YouTube Lectures / वीडियो लेक्चर खोजें:", 
            placeholder="e.g., Structural geology faulting dynamics BSc lectures",
            key="portal_youtube_search"
        )
        
        if yt_query:
            encoded_yt_query = urllib.parse.quote(yt_query.strip())
            YOUTUBE_SYNC_URL = f"https://www.youtube.com/results?search_query={encoded_yt_query}"
            
            st.link_button(
                "📺 Launch Synchronized YouTube Search", 
                YOUTUBE_SYNC_URL, 
                type="secondary", 
                use_container_width=True
            )
        else:
            st.markdown('<div class="highlight-box">⚠️ Enter search query above & Press here to apply!</div>', unsafe_allow_html=True)
            st.button("📺 Terminal Standby (Awaiting Input)", disabled=True, use_container_width=True)

# --- TAB: NEWS & ANNOUNCEMENTS WITH GEMINI ANALYSIS ---
with tab_news:
    st.header("📢 University Bulletins & Notices")
    st.write("Query official notice channels and run cognitive analysis on active institutional releases.")
    
    lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    
    col_n1, col_n2 = st.columns([1, 1])
    
    with col_n1:
        st.subheader("📰 Dynamic Lucknow University Feed")
        if st.button("Query Live Database Feed", type="primary", use_container_width=True):
            scraped_titles = []
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                res = requests.get(lu_url, headers=headers, timeout=10)
                soup = BeautifulSoup(res.content, 'html.parser')
                links = soup.find_all('a', href=True)
                found = 0
                for link in links:
                    if "news" in link['href'] and len(link.text.strip()) > 15:
                        clean_text = link.text.strip().replace("[", "").replace("]", "")
                        href_val = link['href']
                        url = href_val if href_val.startswith('http') else "https://www.lkouniv.ac.in" + href_val
                        st.info(f"🔗 [{clean_text}]({url})")
                        scraped_titles.append(clean_text)
                        found += 1
                    if found > 6: 
                        break
                st.session_state.active_scraped_notices = scraped_titles
            except Exception:
                st.error(f"Live parsing connection error. Access raw terminal index directly: [Lucknow University Notice Board]({lu_url})")
                st.session_state.active_scraped_notices = []
                
    with col_n2:
        st.subheader("🧠 Cognitive AI Notice Interpreter")
        if "active_scraped_notices" in st.session_state and st.session_state.active_scraped_notices:
            st.write("Our cognitive engine can process and classify scraped announcements by critical index levels.")
            if st.button("Run Priority Classifier", type="secondary", use_container_width=True):
                notice_blob = "\n- ".join(st.session_state.active_scraped_notices)
                system_prompt = "You are an administrative coordinator assistant. Categorize these announcements into three tiers: 🔴 Urgent (Exams/Fee deadlines), 🟡 Moderate (Events/Schedules), 🟢 Info (General updates). Keep descriptions extremely brief."
                user_prompt = f"Please categorize these active notices:\n- {notice_blob}"
                with st.spinner("Analyzing semantic structures..."):
                    classification = execute_academic_ai(user_prompt, system_prompt)
                    st.markdown(classification)
        else:
            st.info("Query the Live Database Feed on the left first to enable cognitive notice processing.")

# --- TAB: STUDY MATERIAL ---
with tab_study:
    st.header("📚 Digital Course Assets")
    st.write("Access interconnected institutional cloud infrastructure below.")
    with st.container():
        st.subheader("BSc Management Core")
        st.info("Classroom Code Token: shf3hsat")
        st.link_button("Open Google Classroom Link Structure", "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat", type="primary", use_container_width=True)
    st.caption("Further syllabi data segments are structured automatically upon academic validation.")

# --- TAB: PERFORMANCE TOOLKIT (WITH GEMINI ADVISOR) ---
with tab_perf:
    st.header("🧮 Academic Performance Calculator & Gemini Advisor")
    calc_tab1, calc_tab2, calc_tab3 = st.tabs(["Semester GPA Matrix", "Cumulative CGPA Calculator", "🔮 AI Predictive Insights"])
    
    with calc_tab1:
        st.subheader("Current Semester Track")
        num_courses = st.number_input("Number of Registered Subjects", min_value=1, max_value=10, value=4, step=1)
        scores, credits = [], []
        for i in range(int(num_courses)):
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                score = st.selectbox(f"Grade - Course {i+1}", ["O (Outstanding - 10)", "A+ (Excellent - 9)", "A (Very Good - 8)", "B+ (Good - 7)", "B (Above Average - 6)", "C (Average - 5)", "F (Fail - 0)"], key=f"grade_{i}")
                grade_map = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "F": 0}
                scores.append(grade_map[score.split(" ")[0]])
            with col_c2:
                credit = st.number_input(f"Credits {i+1}", min_value=1, max_value=6, value=4, key=f"credit_{i}")
                credits.append(credit)
        if st.button("Compute Semester Index", type="primary", key="comp_sem_idx", use_container_width=True):
            total_points = sum(s * c for s, c in zip(scores, credits))
            total_credits = sum(credits)
            calculated_gpa = total_points / total_credits if total_credits > 0 else 0
            st.session_state.calculated_term_gpa = calculated_gpa
            st.metric(label="Calculated GPA for Current Term", value=f"{calculated_gpa:.2f} / 10.00")
            
    with calc_tab2:
        st.subheader("Historical CGPA Consolidation")
        prior_cgpa = st.number_input("Current Historical Cumulative CGPA", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        completed_credits = st.number_input("Total Assessment Credits Earned Historically", min_value=0, max_value=200, value=48, step=1)
        st.markdown("---")
        curr_gpa = st.number_input("Latest Term Semester GPA Result", min_value=0.0, max_value=10.0, value=8.5, step=0.1)
        curr_credits = st.number_input("Latest Term Credits Taken", min_value=0, max_value=30, value=20, step=1)
        if st.button("Consolidate Global CGPA", use_container_width=True):
            total_historical_points = prior_cgpa * completed_credits
            total_current_points = curr_gpa * curr_credits
            global_credits = completed_credits + curr_credits
            calculated_cgpa = (total_historical_points + total_current_points) / global_credits if global_credits > 0 else 0
            st.session_state.consolidated_cgpa = calculated_cgpa
            st.metric(label="Updated Aggregate Portfolio CGPA", value=f"{calculated_cgpa:.2f} / 10.00")

    with calc_tab3:
        st.subheader("🔮 Dynamic AI Career & Academic Roadmap")
        st.write("Generate customized study strategy blueprints based on your representative performance metrics.")
        
        target_field = st.selectbox("Your Targeted Postgraduate Field / Goal", ["Geological Survey Research", "Data Analytics & Mathematics", "IIT JAM Preparation", "Public Civil Services Exam"])
        current_gpa_val = st.slider("Select Representative GPA", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
        
        if st.button("Generate Personal Predictive Roadmap", type="primary", use_container_width=True):
            analysis_prompt = f"""
            Act as an academic advisor. The student is tracking with a GPA of {current_gpa_val}/10.00 in {major_focus} ({current_year}).
            Their targeted career milestone is '{target_field}'.
            Provide a 3-step actionable roadmap of recommendations, structural focus zones, or practical research paths. Make it concise.
            """
            with st.spinner("Analyzing learning metrics..."):
                roadmap = execute_academic_ai(analysis_prompt)
                st.markdown(roadmap)

# --- TAB: DEEP FOCUS ENGINE ---
with tab_focus:
    st.header("⏱| Academic Focus Engine")
    
    col_f1, col_f2 = st.columns([2, 1])
    
    with col_f2:
        st.markdown("### 🧠 AI Focus Catalyst")
        current_state = st.selectbox("My Current Cognitive State", ["Exhausted", "Procrastinating", "Anxious", "Highly Focused"])
        if st.button("Generate Focus Catalyst Motivation", type="secondary", use_container_width=True):
            motivation_prompt = f"Synthesize one short, powerful, science-backed productivity tip for a {major_focus} student feeling '{current_state}'. Keep it under 2 sentences."
            with st.spinner("Aligning cognitive states..."):
                catalyst_text = execute_academic_ai(motivation_prompt)
                st.info(catalyst_text)
                
    with col_f1:
        if "timer_running" not in st.session_state: 
            st.session_state.timer_running = False
        duration_selection = st.selectbox("Configure Study Matrix Track:", ["25 Minutes (Standard Study)", "5 Minutes (Short Break)", "15 Minutes (Extended Intermission)"])
        duration_map = {"25": 25 * 60, "5": 5 * 60, "15": 15 * 60}
        target_seconds = duration_map[duration_selection.split(" ")[0]]
        progress_bar = st.progress(0.0)
        timer_display = st.empty()
        
        if st.button("Initialize Focus Session Pipeline", type="primary", use_container_width=True):
            st.session_state.timer_running = True
            start_time = time.time()
            while st.session_state.timer_running:
                elapsed = time.time() - start_time
                remaining = target_seconds - elapsed
                if remaining <= 0:
                    st.session_state.timer_running = False
                    progress_bar.progress(1.0)
                    timer_display.subheader("⏱️ Session Finalized! Re-allocate tasks.")
                    st.balloons()
                    break
                mins, secs = divmod(int(remaining), 60)
                timer_display.markdown(f"<h1 style='font-size:42px; font-weight:700;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
                progress_bar.progress(min(elapsed / target_seconds, 1.0))
                time.sleep(1)

# --- TAB: REPORT REGISTRATION ISSUE ---
with tab_report:
    st.header("🚨 Administrative Issue Escalation")
    with st.form("issue_form", clear_on_submit=False):
        student_email = st.text_input("Your Email Address *", placeholder="student@example.com")
        name = st.text_input("Full Name *")
        roll_no = st.text_input("Roll Number / Student ID *")
        issue_type = st.selectbox("Issue Category", ["Login Problem", "Subject Not Showing", "Document Error", "Other"])
        details = st.text_area("Detailed Description *")
        submitted = st.form_submit_button("Submit & Notify Admin", use_container_width=True)
    if submitted:
        if student_email and name and roll_no and details:
            email_payload = {"email": student_email.strip(), "Student Name": name.strip(), "Roll Number": roll_no.strip(), "Issue Type": issue_type, "Detailed Description": details.strip(), "_subject": f"🚨 Urgent: Registration Issue from {name.strip()}", "_captcha": "false"}
            with st.spinner("Processing form with target server..."):
                try:
                    response = requests.post(f"https://formsubmit.co/ajax/{ADMIN_EMAIL}", data=email_payload, timeout=10)
                    if response.status_code == 200: st.toast("Form processed! Email confirmation sent.", icon="📧")
                    else: st.error(f"Endpoint verification issue encountered. Status Code: {response.status_code}")
                except Exception: st.error("Automated transmission pipeline timeout. Proceeding to alternative routing.")
            wa_text = f"*Registration Issue Report*\n\n*Name:* {name}\n*Roll No:* {roll_no}\n*Email:* {student_email}\n*Issue:* {issue_type}\n*Details:* {details}"
            wa_url = f"https://wa.me/{ADMIN_PHONE}?text={urllib.parse.quote(wa_text)}"
            st.success("🎉 Local data entry recorded successfully!")
            st.link_button("Finalize via WhatsApp Message ✅", wa_url, use_container_width=True)
            st.balloons()
        else: st.error("⚠️ Validation failure: Please fill out all required fields marked with (*).")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='font-size: 11px;'>Powered by Google Workspace and Microhnm Technologies</center>", unsafe_allow_html=True)
import streamlit as st

from knowledge_gpt.components.sidebar import sidebar

from knowledge_gpt.ui import (
    wrap_doc_in_html,
    is_query_valid,
    is_file_valid,
    is_open_ai_key_valid,
    display_file_read_error,
)

from knowledge_gpt.core.caching import bootstrap_caching

from knowledge_gpt.core.parsing import read_file
from knowledge_gpt.core.chunking import chunk_file
from knowledge_gpt.core.embedding import embed_files
from knowledge_gpt.core.qa import query_folder
from knowledge_gpt.core.utils import get_llm


EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="KnowledgeGPT", page_icon="📖", layout="wide")
st.header("📖KnowledgeGPT")

# Enable caching for expensive functions
bootstrap_caching()

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")


if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )


uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
)

model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

with st.expander("Advanced Options"):
    return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")


if not uploaded_file:
    st.stop()

try:
    file = read_file(uploaded_file)
except Exception as e:
    display_file_read_error(e, file_name=uploaded_file.name)

chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

if not is_file_valid(file):
    st.stop()


if not is_open_ai_key_valid(openai_api_key, model):
    st.stop()


with st.spinner("Indexing document... This may take a while⏳"):
    folder_index = embed_files(
        files=[chunked_file],
        embedding=EMBEDDING if model != "debug" else "debug",
        vector_store=VECTOR_STORE if model != "debug" else "debug",
        openai_api_key=openai_api_key,
    )

with st.form(key="qa_form"):
    query = st.text_area("Ask a question about the document")
    submit = st.form_submit_button("Submit")


if show_full_doc:
    with st.expander("Document"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)


if submit:
    if not is_query_valid(query):
        st.stop()

    # Output Columns
    answer_col, sources_col = st.columns(2)

    llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
    result = query_folder(
        folder_index=folder_index,
        query=query,
        return_all=return_all_chunks,
        llm=llm,
    )

    with answer_col:
        st.markdown("#### Answer")
        st.markdown(result.answer)

    with sources_col:
        st.markdown("#### Sources")
        for source in result.sources:
            st.markdown(source.page_content)
            st.markdown(source.metadata["source"])
            st.markdown("---")
