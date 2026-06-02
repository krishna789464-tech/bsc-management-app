import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time
import streamlit.components.v1 as components
from PIL import Image

# --- 1. CONFIGURATION & STYLING ---
LOGO_PATH = r"C:\Users\ADMIN\Desktop\app logo.png"

logo_exists = os.path.exists(LOGO_PATH)
if logo_exists:
    app_logo = Image.open(LOGO_PATH)
    page_icon_val = app_logo
else:
    app_logo = None
    page_icon_val = "🎓"

st.set_page_config(
    page_title="Academic Student Portal",
    page_icon=page_icon_val,
    layout="wide"
)

# Professional Enterprise Theme Styling
st.markdown("""
    <style>
    /* Global App Background */
    .stApp { background-color: #f8fafc; }
    
    /* Clean Main Interface Cards */
    .main-card { 
        padding: 24px; 
        border-radius: 12px; 
        background: #ffffff; 
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05), 0 1px 2px 0 rgba(0,0,0,0.03);
        border: 1px solid #e2e8f0;
    }
    
    /* Metrics Interface */
    .metric-card { 
        background: #ffffff; 
        padding: 22px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        text-align: center; 
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    /* Structural Professional Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 8px;
    }
    .sidebar-meta {
        font-size: 13px;
        color: #475569;
        background-color: #f1f5f9;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 24px;
        border: 1px solid #e2e8f0;
    }
    
    /* --- INVISIBLE HEADERS / DE-BRANDING STREAMLIT --- */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    
    /* Clean up form spacing */
    .stForm {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 24px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE TARGET CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"

# --- 2. SIDEBAR NAVIGATION ---
if logo_exists and app_logo:
    st.logo(LOGO_PATH) 
else:
    st.sidebar.markdown("<h2 style='margin-top: 0; color: #2563eb; font-weight:700;'>🎓 System Portal</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-meta">
        <strong style="color:#0f172a;">🏫 Portal Verification</strong><br>
        <span style="opacity: 0.85; font-size:12px;">Access Tier: B.Sc Undergraduate</span><br>
        <hr style="margin: 10px 0; border: 0; border-top: 1px solid #cbd5e1;">
        <strong style="color:#0f172a;">📧 Helpdesk Routing</strong><br>
        <a href="mailto:{ADMIN_EMAIL}" style="color: #2563eb; text-decoration: none; font-size:12px;">{ADMIN_EMAIL}</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-weight: 700; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 8px; color:#64748b;'>CORE WORKSPACES</p>", unsafe_allow_html=True)

# Navigation Engine Array
page = st.sidebar.radio(
    label="Navigation Menu",
    options=[
        "📊 Student Dashboard", 
        "🤖 AI Academic Assistant", 
        "📢 News & Notices", 
        "📚 Study Classrooms", 
        "🧮 Performance Toolkit", 
        "⏱️ Deep Focus Engine", 
        "🚨 Report Routing Terminal"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("<div style='flex:1;'></div>", unsafe_allow_html=True)
st.sidebar.caption("System Status: Operational • v2.1.0")


# --- PAGE: DASHBOARD ---
if page == "📊 Student Dashboard":
    st.title("Welcome to the Dashboard")
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 32px; border-radius: 16px; margin-bottom: 28px;">
            <h1 style="margin: 0; color: white; font-weight:700; font-size:28px;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.9; margin-top: 8px; font-size: 15px; max-width: 700px;">
                Central administrative hub optimized for real-time classroom updates, digital asset access, performance management, and direct administrative escalation pathways.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h4 style="color:#64748b; margin:0; font-size:14px;">Total Cohort</h4><h1 style="color: #2563eb; margin:8px 0 0 0; font-weight:700;">1,250</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4 style="color:#64748b; margin:0; font-size:14px;">Active Courses</h4><h1 style="color: #16a34a; margin:8px 0 0 0; font-weight:700;">18</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h4 style="color:#64748b; margin:0; font-size:14px;">Active System Notices</h4><h1 style="color: #ea580c; margin:8px 0 0 0; font-weight:700;">6</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h4 style="color:#64748b; margin:0; font-size:14px;">Pending Form Inquiries</h4><h1 style="color: #dc2626; margin:8px 0 0 0; font-weight:700;">12</h1></div>', unsafe_allow_html=True)
        
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


# --- PAGE: AI ASSISTANT ---
elif page == "🤖 AI Academic Assistant":
    st.header("🤖 AI Student Counselor & Helper")
    st.write("Our automated academic agent is loading below. If it does not open automatically, please look for a chat icon on the screen.")
    
    jotform_script = """
    <script
      src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'>
    </script>
    """
    components.html(jotform_script, height=600, scrolling=True)


# --- PAGE: NEWS & ANNOUNCEMENTS ---
elif page == "📢 News & Notices":
    st.header("📢 University Bulletins & Notices")
    lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    
    if st.button("Query Live Database Feed", type="primary"):
        try:
            res = requests.get(lu_url, timeout=10)
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


# --- PAGE: STUDY MATERIAL ---
elif page == "📚 Study Classrooms":
    st.header("📚 Digital Course Assets")
    st.write("Access interconnected institutional cloud infrastructure below.")
    
    with st.container():
        st.subheader("BSc Management Core")
        st.info("Classroom Code Token: shf3hsat")
        st.link_button("Open Google Classroom Link Structure", "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat", type="primary")
    
    st.divider()
    st.caption("Further syllabi data segments are structured automatically upon academic validation.")


# --- NEW FEATURE: PERFORMANCE TOOLKIT (GPA/CGPA CALCULATOR) ---
elif page == "🧮 Performance Toolkit":
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
                # Map select box value to numerical point structure
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


# --- NEW FEATURE: DEEP FOCUS ENGINE (POMODORO TIMER) ---
elif page == "⏱️ Deep Focus Engine":
    st.header("⏱️ Academic Focus Engine")
    st.write("Utilize timed intervals to optimize reading or research sessions.")
