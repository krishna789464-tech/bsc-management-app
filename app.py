import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import google.generativeai as genai
import os

# --- 1. CONFIGURATION & STYLING ---
LOGO_PATH = r"C:\Users\ADMIN\Desktop\app logo.png"

if not os.path.exists(LOGO_PATH):
    LOGO_PATH = "🎓"

st.set_page_config(
    page_title="Company Dashboard",
    page_icon=LOGO_PATH,
    layout="wide"
)

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
DEFAULT_API_KEY = st.secrets.get("GEMINI_API_KEY", "AQ.Ab8RN6KSEnxgUh1R98MZigwwsySa2gu9PpW4eWTWkR9GsDvNQA")

# --- 2. SIDEBAR NAVIGATION & AI PROMPT CONTROL ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.info(f"Admin: {ADMIN_EMAIL}")

st.sidebar.subheader("⚙️ AI System Prompt Configuration")
default_instructions = (
    "You are an empathetic, knowledgeable, and dedicated academic helper and counselor "
    "for B.Sc Management students at Lucknow University. Provide actionable, supportive, "
    "and accurate answers to the student's request."
)

custom_system_prompt = st.sidebar.text_area(
    "Master AI Commands / Instructions:",
    value=default_instructions,
    help="Edit this text to change the hidden rule-set governing how the AI responds to students.",
    height=150
)

user_api_key = st.sidebar.text_input("Gemini API Key (Leave blank for default)", type="password")
ACTIVE_API_KEY = user_api_key.strip() if user_api_key.strip() else DEFAULT_API_KEY

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
