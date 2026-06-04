import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time
import streamlit.components.v1 as components
from PIL import Image

# --- 1. ACCESSIBILITY & BRIGHTNESS SESSION STATE ---
if "font_scale" not in st.session_state:
    st.session_state.font_scale = 100  # Default font percentage
if "bg_theme" not in st.session_state:
    st.session_state.bg_theme = "light"  # Default theme
if "animation_played" not in st.session_state:
    st.session_state.animation_played = False

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

# Theme Configuration Colors
if st.session_state.bg_theme == "light":
    bg_color = "#f1f5f9"
    card_bg = "#ffffff"
    text_color = "#0f172a"
    sub_text_color = "#475569"
    border_color = "#cbd5e1"
    tab_active_text = "#ffffff"
else:
    bg_color = "#0b0f19"
    card_bg = "#161e2e"
    text_color = "#f8fafc"
    sub_text_color = "#94a3b8"
    border_color = "#2d3748"
    tab_active_text = "#ffffff"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: {st.session_state.font_scale}% !important;
    }}
    h1 {{ font-size: 2rem !important; color: {text_color} !important; font-weight: 700 !important; }}
    h2 {{ font-size: 1.6rem !important; color: {text_color} !important; font-weight: 700 !important; }}
    h3 {{ font-size: 1.25rem !important; color: {text_color} !important; font-weight: 600 !important; }}
    h4 {{ font-size: 1.1rem !important; color: {text_color} !important; font-weight: 600 !important; }}
    p, span, label, li, td {{ color: {text_color} !important; }}
    .stApp {{ background-color: {bg_color} !important; }}
    [data-testid="stHeader"] {{ display: none !important; height: 0px !important; }}
    .block-container {{ padding-top: 1rem !important; padding-bottom: 2rem !important; }}
    .main-card {{ padding: 20px; border-radius: 12px; background: {card_bg}; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid {border_color}; }}
    .metric-card {{ background: {card_bg} !important; padding: 18px; border-radius: 12px; text-align: center; border: 1px solid {border_color} !important; margin-bottom: 12px; }}
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {{ gap: 6px; background-color: {card_bg}; padding: 6px; border-radius: 12px; border: 1px solid {border_color}; }}
    div[data-testid="stTabs"] [data-baseweb="tab"] {{ padding: 6px 12px; border-radius: 8px; font-weight: 500; color: {sub_text_color} !important; }}
    div[data-testid="stTabs"] [aria-selected="true"] {{ background-color: #2563eb !important; color: {tab_active_text} !important; }}
    div[data-testid="stAppDeployButton"] {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; }}
    footer {{ visibility: hidden !important; }}
    .stForm {{ background: {card_bg} !important; border: 1px solid {border_color} !important; border-radius: 12px !important; padding: 20px !important; }}
    </style>
    """, unsafe_allow_html=True)

ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"
NOTEBOOK_LM_URL = "https://notebooklm.google.com/notebook/4865426e-ee8e-4256-956c-9f09f7c6c332?addSource=true"

# Running Clock Markup
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
st.warning("⚠️ **System Notice / आवश्यक सूचना:** This portal is currently in the **testing phase**. (यह एप्लिकेशन अभी टेस्टिंग फेज़ में है।)")

# --- UPDATED APP NAVIGATION NAVIGATION TABS ---
tabs = st.tabs([
    "📊 Dashboard",
    "🤖 AI Assistant",
    "🔍 Deep Search (NotebookLM)",
    "📢 News & Notices",
    "📚 Study Classrooms",
    "🧮 Performance Toolkit",
    "⏱️ Focus Engine",
    "🚨 Report Issue"
])
tab_dashboard, tab_ai, tab_deep_search, tab_news, tab_study, tab_perf, tab_focus, tab_report = tabs

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

# --- TAB: AI ASSISTANT ---
with tab_ai:
    st.header("🤖 AI Student Counselor")
    st.write("Our automated academic agent is loading below. If it does not open automatically, look for the chat container asset.")
    jotform_script = "<script src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'></script>"
    components.html(jotform_script, height=550, scrolling=True)

# --- NEW TAB: DEDICATED DEEP SEARCH (GOOGLE NOTEBOOKLM) ---
with tab_deep_search:
    st.header("🔍 Deep Search & NotebookLM Environment")
    st.write("Stage assets locally and connect directly to your automated Google notebook indexing cluster.")
    
    search_left, search_right = st.columns([1.6, 1.4])
    
    
        # Application Text Command Box
        user_command = st.text_area(
            "Type your execution query or analytical prompt below:",
            placeholder="e.g., Cross-examine these notes and construct a 5-point study summary highlighting structural vulnerabilities.",
            key="notebook_text_command"
        )
        
        if user_command:
            # Clipboard utility copy logic helper
            st.info("💡 Your text query is saved below. Click 'Launch' to bridge and process your dataset.")

    with search_right:
        st.subheader("🌐 Sync & Gateway Pipeline")
        st.markdown(f"""
            <div style="border: 1px solid {border_color}; background-color: {card_bg}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
                <h4 style="margin-top:0; color:#2563eb;">Pipeline Initialization Status</h4>
                <p style="font-size:0.9rem; line-height:1.5; margin-bottom:12px;">
                    Google NotebookLM enforces rigorous browser isolation protocols. To sync data, use this staging block to structure notes, then forward execution to the primary interface.
                </p>
                <span style="font-size:0.8rem; background-color:#dcfce7; color:#15803d; padding:4px 8px; border-radius:6px; font-weight:600;">🔗 Environment Bridge Available</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Gateway Action Button
        if st.link_button(
            "🚀 Launch Connected NotebookLM Chat Session", 
            NOTEBOOK_LM_URL, 
            type="primary", 
            use_container_width=True
        ):
            if uploaded_files or user_command:
                st.toast("Pipeline launched! Drop your staged files into the source window.", icon="⚙️")
# Replace your tab_deep_search block with this optimized UI layout

with tab_deep_search:
    st.header("🔍 Deep Search & NotebookLM Gateway")
    st.write("Prepare your workspace assets below to sync with Google NotebookLM.")
    
    col_left, col_right = st.columns([1.5, 1.5])
    
    with col_left:
        st.subheader("1. Stage Your Files & Prompt")
        
        # Local file staging
        uploaded_files = st.file_uploader(
            "Drag your study files here first:", 
            accept_multiple_files=True,
            key="nb_uploader"
        )
        
        if uploaded_files:
            st.success(f"📋 {len(uploaded_files)} file(s) ready in staging area.")
            # Displaying files clearly so user can drag them out if browser supports it, 
            # or remember what to drop into NotebookLM.
            for f in uploaded_files:
                st.caption(f"📄 **{f.name}** (Ready to drop)")
        
        # Command Text Input
        user_command = st.text_area(
            "Type the command you want executed automatically:",
            placeholder="e.g., Summarize the key concepts of faulting dynamics from these notes.",
            key="nb_command"
        )

    with col_right:
        st.subheader("2. Execute Automated Sync")
        st.markdown(f"""
            <div style="border: 1px solid {border_color}; background-color: {card_bg}; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h5 style="margin:0; color:#2563eb;">How it works:</h5>
                <ol style="font-size: 0.85rem; padding-left: 20px; margin-top: 5px;">
                    <li>Click the <b>Launch</b> button below.</li>
                    <li>NotebookLM will open, and your text command will <b>auto-type and submit itself</b> via your browser script.</li>
                    <li>Drag your staged files from your desktop directly into the NotebookLM source panel.</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        
        if user_command:
            # Safely encode the text query for the address bar
            encoded_query = urllib.parse.quote(user_command)
            # Append the portal query parameter to your specific NotebookLM URL
            AUTOMATED_URL = f"{NOTEBOOK_LM_URL}&portalQuery={encoded_query}"
            
            st.link_button(
                "🚀 Launch & Auto-Type Command", 
                AUTOMATED_URL, 
                type="primary", 
                use_container_width=True
            )
        else:
            st.button("🚀 Launch & Auto-Type Command", disabled=True, use_container_width=True)
            st.caption("⚠️ Please write a command prompt on the left to activate the launch pipeline.")
# --- TAB: NEWS & ANNOUNCEMENTS ---
with tab_news:
    st.header("📢 University Bulletins & Notices")
    lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    if st.button("Query Live Database Feed", type="primary", use_container_width=True):
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
                    found += 1
                if found > 10: break
        except Exception:
            st.error(f"Live parsing connection error. Access raw terminal index directly: [Lucknow University Notice Board]({lu_url})")

# --- TAB: STUDY MATERIAL ---
with tab_study:
    st.header("📚 Digital Course Assets")
    st.write("Access interconnected institutional cloud infrastructure below.")
    with st.container():
        st.subheader("BSc Management Core")
        st.info("Classroom Code Token: shf3hsat")
        st.link_button("Open Google Classroom Link Structure", "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat", type="primary", use_container_width=True)
    st.divider()
    st.caption("Further syllabi data segments are structured automatically upon academic validation.")

# --- TAB: PERFORMANCE TOOLKIT ---
with tab_perf:
    st.header("🧮 Academic Performance Calculator")
    calc_tab1, calc_tab2 = st.tabs(["Semester GPA Matrix", "Cumulative CGPA Calculator"])
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
        if st.button("Compute Semester Index", type="primary", use_container_width=True):
            total_points = sum(s * c for s, c in zip(scores, credits))
            total_credits = sum(credits)
            calculated_gpa = total_points / total_credits if total_credits > 0 else 0
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
            st.metric(label="Updated Aggregate Portfolio CGPA", value=f"{calculated_cgpa:.2f} / 10.00")

# --- TAB: DEEP FOCUS ENGINE ---
with tab_focus:
    st.header("⏱️ Academic Focus Engine")
    if "timer_running" not in st.session_state: st.session_state.timer_running = False
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
st.markdown("<center style='font-size: 11px;'>Powered by Google Workspace Infrastructure and Microhnm Technologies</center>", unsafe_allow_html=True)
