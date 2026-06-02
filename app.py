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
    st.session_state.bg_theme = "light"  # Default brightness theme

# --- 2. CONFIGURATION & STYLING ---
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

# Theme Background & Font Scaling Calculations
bg_color = "#f8fafc" if st.session_state.bg_theme == "light" else "#0f172a"
card_bg = "#ffffff" if st.session_state.bg_theme == "light" else "#1e293b"
text_color = "#1e293b" if st.session_state.bg_theme == "light" else "#f1f5f9"
sub_text_color = "#64748b" if st.session_state.bg_theme == "light" else "#94a3b8"
border_color = "#e2e8f0" if st.session_state.bg_theme == "light" else "#334155"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');

    /* Global Accessibility Adjustments */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], p, span, label, h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', sans-serif !important;
        font-size: {st.session_state.font_scale}% !important;
        color: {text_color} !important;
    }}

    .stApp {{
        background-color: {bg_color} !important;
    }}

    /* Main Dashboard Layout Blocks */
    .main-card {{
        padding: 24px;
        border-radius: 12px;
        background: {card_bg};
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);
        border: 1px solid {border_color};
    }}

    .metric-card {{
        background: {card_bg} !important;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        text-align: center;
        border: 1px solid {border_color} !important;
        transition: transform 0.2s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
    }}
    .metric-card h4 {{
        color: {sub_text_color} !important;
    }}

    /* Top Tabs Styling adjustment based on color configuration selection */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: {card_bg};
        padding: 8px;
        border-radius: 12px;
        border: 1px solid {border_color};
    }}

    div[data-testid="stTabs"] [data-baseweb="tab"] {{
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 500;
        color: {sub_text_color} !important;
    }}

    div[data-testid="stTabs"] [aria-selected="true"] {{
        background-color: #2563eb !important;
        color: white !important;
    }}

    /* Floating Panel container targeted strictly to top-right corner wrapper */
    div.floating-control-container {{
        position: fixed;
        top: 60px;
        right: 20px;
        z-index: 999999;
        background-color: {card_bg};
        padding: 12px 18px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid {border_color};
        max-width: 300px;
    }}

    /* Hide unneeded default branding frames wrapper */
    div[data-testid="stAppDeployButton"] {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; }}
    footer {{ visibility: hidden !important; }}

    .stForm {{
        background: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 24px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SECURE TARGET CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"

# --- 3. DYNAMIC TOP-RIGHT SYSTEM CONTROLS WORKFLOW ---
# Creating an isolated structural column right above the workspace framework to host the control menu natively
with st.sidebar:
    # Optional fallback toggle just in case the floating layout gets covered by screen items
    st.markdown("### ⚙️ Quick System View")
    st.write("Adjust themes via the floating widget in the top right window quadrant contextually.")

# Rendering the floating control block dynamically on screen using columns
st.markdown('<div class="floating-control-container">', unsafe_allow_html=True)
c_control1, c_control2 = st.columns(2)
with c_control1:
    theme_choice = st.selectbox(
        "Brightness", 
        ["☀️ Light Mode", "🌙 Dark Mode"], 
        index=0 if st.session_state.bg_theme == "light" else 1,
        key="theme_select_widget"
    )
    new_theme = "light" if "Light" in theme_choice else "dark"
    if new_theme != st.session_state.bg_theme:
        st.session_state.bg_theme = new_theme
        st.rerun()

with c_control2:
    font_choice = st.selectbox(
        "Text Size", 
        ["Normal (100%)", "Large (120%)", "Huge (140%)"],
        index=0 if st.session_state.font_scale == 100 else (1 if st.session_state.font_scale == 120 else 2),
        key="font_select_widget"
    )
    new_scale = 100 if "Normal" in font_choice else (120 if "Large" in font_choice else 140)
    if new_scale != st.session_state.font_scale:
        st.session_state.font_scale = new_scale
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. HEADER BRANDING ---
st.markdown(f"<h2 style='margin: 0; color: #1e3a8a; font-weight:700;'>🎓 Academic Student Portal</h2>", unsafe_allow_html=True)
st.markdown(f"Verification Tier: B.Sc Undergraduate • Helpdesk: <a href='mailto:{ADMIN_EMAIL}' style='color:#2563eb;'>{ADMIN_EMAIL}</a>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- 5. TOP TABS NAVIGATION ---
tabs = st.tabs([
    "📊 Dashboard",
    "🤖 AI Assistant",
    "📢 News & Notices",
    "📚 Study Classrooms",
    "🧮 Performance Toolkit",
    "⏱️ Focus Engine",
    "🚨 Report Issue"
])

tab_dashboard, tab_ai, tab_news, tab_study, tab_perf, tab_focus, tab_report = tabs

# --- TAB: DASHBOARD ---
with tab_dashboard:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); color: white !important; padding: 32px; border-radius: 16px; margin-bottom: 28px; margin-top: 10px;">
            <h1 style="margin: 0; color: white !important; font-weight:700; font-size:28px;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.9; margin-top: 8px; font-size: 15px; max-width: 700px; color: white !important;">
                Central administrative hub optimized for real-time classroom updates, digital asset access, performance management, and direct administrative escalation pathways.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h4>Total Cohort</h4><h1 style="color: #2563eb !important; margin:8px 0 0 0; font-weight:700;">1,250</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>Active Courses</h4><h1 style="color: #16a34a !important; margin:8px 0 0 0; font-weight:700;">18</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h4>Active System Notices</h4><h1 style="color: #ea580c !important; margin:8px 0 0 0; font-weight:700;">6</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h4>Pending Form Inquiries</h4><h1 style="color: #dc2626 !important; margin:8px 0 0 0; font-weight:700;">12</h1></div>', unsafe_allow_html=True)
        
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
    st.header("🤖 AI Student Counselor & Helper")
    st.write("Our automated academic agent is loading below. If it does not open automatically, please look for a chat icon on the screen.")
    
    jotform_script = """
    <script src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'>
    </script>
    """
    components.html(jotform_script, height=600, scrolling=True)

# --- TAB: NEWS & ANNOUNCEMENTS ---
with tab_news:
    st.header("📢 University Bulletins & Notices")
    lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    
    if st.button("Query Live Database Feed", type="primary"):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
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
                if found > 10: 
                    break
        except Exception:
            st.error(f"Live parsing connection error. Access raw terminal index directly: [Lucknow University Notice Board]({lu_url})")

# --- TAB: STUDY MATERIAL ---
with tab_study:
    st.header("📚 Digital Course Assets")
    st.write("Access interconnected institutional cloud infrastructure below.")
    with st.container():
        st.subheader("BSc Management Core")
        st.info("Classroom Code Token: shf3hsat")
        st.link_button("Open Google Classroom Link Structure", "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat", type="primary")
    st.divider()
    st.caption("Further syllabi data segments are structured automatically upon academic validation.")

# --- TAB: PERFORMANCE TOOLKIT ---
with tab_perf:
    st.header("🧮 Academic Performance Calculator")
    st.write("Calculate estimated Grade Point Average (GPA) and Cumulative values securely.")
    
    calc_tab1, calc_tab2 = st.tabs(["Semester GPA Matrix", "Cumulative CGPA Calculator"])
    
    with calc_tab1:
        st.subheader("Current Semester Track")
        num_courses = st.number_input("Number of Registered Subjects", min_value=1, max_value=10, value=4, step=1)
        scores = []
        credits = []
        
        col_c1, col_c2 = st.columns(2)
        for i in range(int(num_courses)):
            with col_c1:
                score = st.selectbox(f"Letter Grade - Course {i+1}", ["O (Outstanding - 10)", "A+ (Excellent - 9)", "A (Very Good - 8)", "B+ (Good - 7)", "B (Above Average - 6)", "C (Average - 5)", "F (Fail - 0)"], key=f"grade_{i}")
                grade_map = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "F": 0}
                scores.append(grade_map[score.split(" ")[0]])
            with col_c2:
                credit = st.number_input(f"Course Weight / Credits {i+1}", min_value=1, max_value=6, value=4, key=f"credit_{i}")
                credits.append(credit)
                
        if st.button("Compute Semester Index", type="primary"):
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
        
        if st.button("Consolidate Global CGPA"):
            total_historical_points = prior_cgpa * completed_credits
            total_current_points = curr_gpa * curr_credits
            global_credits = completed_credits + curr_credits
            calculated_cgpa = (total_historical_points + total_current_points) / global_credits if global_credits > 0 else 0
            st.metric(label="Updated Aggregate Portfolio CGPA", value=f"{calculated_cgpa:.2f} / 10.00")

# --- TAB: DEEP FOCUS ENGINE ---
with tab_focus:
    st.header("⏱️ Academic Focus Engine")
    st.write("Utilize timed intervals to optimize reading or research sessions.")
    
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
        
    duration_selection = st.selectbox("Configure Study Matrix Track:", ["25 Minutes (Standard Study)", "5 Minutes (Short Break)", "15 Minutes (Extended Intermission)"])
    duration_map = {"25": 25 * 60, "5": 5 * 60, "15": 15 * 60}
    target_seconds = duration_map[duration_selection.split(" ")[0]]
    
    progress_bar = st.progress(0.0)
    timer_display = st.empty()
    
    if st.button("Initialize Focus Session Pipeline", type="primary"):
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
            timer_display.markdown(f"<h1 style='font-size:48px; color:#1e40af;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            percentage_completion = min(elapsed / target_seconds, 1.0)
            progress_bar.progress(percentage_completion)
            time.sleep(1)

# --- TAB: REPORT REGISTRATION ISSUE ---
with tab_report:
    st.header("🚨 Administrative Issue Escalation")
    st.write("Submit technical issues below to register tickets and initialize support workflows.")
    
    with st.form("issue_form", clear_on_submit=False):
        student_email = st.text_input("Your Email Address *", placeholder="student@example.com")
        name = st.text_input("Full Name *")
        roll_no = st.text_input("Roll Number / Student ID *")
        issue_type = st.selectbox("Issue Category", ["Login Problem", "Subject Not Showing", "Document Error", "Other"])
        details = st.text_area("Detailed Description *")
        submitted = st.form_submit_button("Submit & Notify Admin")
        
    if submitted:
        if student_email and name and roll_no and details:
            email_payload = {
                "email": student_email.strip(),
                "Student Name": name.strip(),
                "Roll Number": roll_no.strip(),
                "Issue Type": issue_type,
                "Detailed Description": details.strip(),
                "_subject": f"🚨 Urgent: Registration Issue from {name.strip()}",
                "_captcha": "false"
            }
            
            with st.spinner("Processing form with target server..."):
                try:
                    response = requests.post(
                        f"https://formsubmit.co/ajax/{ADMIN_EMAIL}", 
                        data=email_payload, 
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.toast("Form processed! Email confirmation sent.", icon="📧")
                    else:
                        st.error(f"Endpoint verification issue encountered. Status Code: {response.status_code}")
                except Exception:
                    st.error("Automated transmission pipeline timeout. Proceeding to direct alternative routing.")
                    
            wa_text = f"*Registration Issue Report*\n\n*Name:* {name}\n*Roll No:* {roll_no}\n*Email:* {student_email}\n*Issue:* {issue_type}\n*Details:* {details}"
            wa_url = f"https://wa.me/{ADMIN_PHONE}?text={urllib.parse.quote(wa_text)}"
            
            st.success("🎉 Local data entry recorded successfully!")
            st.write("Click below to pass execution control to WhatsApp and notify the Admin directly:")
            st.link_button("Finalize via WhatsApp Message ✅", wa_url)
            st.balloons()
        else:
            st.error("⚠️ Validation failure: Please fill out all required fields marked with (*).")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='color: #94a3b8; font-size: 12px;'>Powered by Google Workspace Infrastructure and Microhnm Technologies</center>", unsafe_allow_html=True)
