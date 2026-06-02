import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import streamlit.components.v1 as components
from PIL import Image

# --- 1. CONFIGURATION & STYLING ---
# Target local logo image location dynamically across absolute paths securely
LOGO_PATH = r"C:\Users\ADMIN\Desktop\app logo.png"

# Fallback mechanism to keep the application from crashing if the file is moved or renamed
logo_exists = os.path.exists(LOGO_PATH)
if logo_exists:
    # Open the image using PIL for native browser tab support
    app_logo = Image.open(LOGO_PATH)
    page_icon_val = app_logo
else:
    app_logo = None
    page_icon_val = "🎓" # Fallback to a default emoji if path is missing

st.set_page_config(
    page_title="Company Dashboard",
    page_icon=page_icon_val,
    layout="wide"
)

# Render the application logo inside the navigation sidebar if the file exists
if logo_exists and app_logo:
    st.logo(LOGO_PATH)
else:
    st.sidebar.markdown("# 🎓") # Fallback icon header if file is missing

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE TARGET CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.info(f"Admin: {ADMIN_EMAIL}")

page = st.sidebar.radio("Go to:", ["Dashboard", "AI Assistant", "News & Announcements", "Study Material", "Report Registration Issue"])

# --- PAGE: DASHBOARD ---
if page == "Dashboard":
    st.title("Welcome to the Dashboard")
    st.markdown("""
        <div style="background: linear-gradient(to right, #2563eb, #4f46e5); color: white; padding: 30px; border-radius: 20px; margin-bottom: 25px;">
            <h1 style="margin: 0; color: white;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.9; margin-top: 5px; font-size: 16px;">
                Smart academic platform for study materials, notices, classroom access, and student issue management.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>Students</h3><h1 style="color: #2563eb; margin:0;">1,250</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Courses</h3><h1 style="color: #16a34a; margin:0;">18</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>Notices</h3><h1 style="color: #ea580c; margin:0;">6</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>Pending Issues</h3><h1 style="color: #dc2626; margin:0;">12</h1></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("📚 Quick Overview: Connected Materials")
        materials = [
            {"subject": "Structural Geology", "teacher": "Dr. Sharma"},
            {"subject": "Mineralogy", "teacher": "Prof. Singh"},
            {"subject": "Engineering Mathematics", "teacher": "Dr. Verma"}
        ]
        for item in materials:
            with st.container():
                st.markdown(f"**{item['subject']}** — Teacher: {item['teacher']}")
                st.caption("🟢 Google Classroom Sync Active")
                st.divider()
                
    with right_col:
        st.subheader("⚡ Quick Access Controls")
        st.button("📋 Attendance Tracker", use_container_width=True)
        st.button("📝 Assignment Portal", use_container_width=True)
        st.button("📅 Academic Timetable", use_container_width=True)
        st.button("📊 Examination Results", use_container_width=True)

# --- PAGE: AI ASSISTANT (JOTFORMS EMBED) ---
elif page == "AI Assistant":
    st.header("🤖 AI Student Counselor & Helper")
    st.write("Our automated academic agent is loading below. If it does not open automatically, please look for a chat icon on the screen.")
    
    jotform_script = """
    <script
      src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'>
    </script>
    """
    components.html(jotform_script, height=600, scrolling=True)

# --- PAGE: NEWS & ANNOUNCEMENTS ---
elif page == "News
