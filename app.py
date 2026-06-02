import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time
import streamlit.components.v1 as components
from PIL import Image

# --- 1. CONFIGURATION & STYLING ---
# File path check ko secure banaya taaki local path missing hone par app crash na ho
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

# Professional Enterprise Theme Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background-color: #f8fafc;
    }

    .main-card {
        padding: 24px;
        border-radius: 12px;
        background: #ffffff;
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05), 0 1px 2px 0 rgba(0,0,0,0.03);
        border: 1px solid #e2e8f0;
    }

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

    /* Top Navigation bar customization */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }

    div[data-testid="stTabs"] [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 500;
        color: #475569;
    }

    div[data-testid="stTabs"] [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }

    /* Hide branding safely */
    div[data-testid="stAppDeployButton"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    footer { visibility: hidden !important; }

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

# --- 2. TOP HEADER BRANDING ---
st.markdown("<h2 style='margin: 0; color: #1e3a8a; font-weight:700;'>🎓 Academic Student Portal</h2>", unsafe_allow_html=True)
st.markdown(f"Verification Tier: B.Sc Undergraduate • Helpdesk: <a href='mailto:{ADMIN_EMAIL}'>{ADMIN_EMAIL}</a>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- 3. TOP TABS NAVIGATION ---
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
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 32px; border-radius: 16px; margin-bottom: 28px; margin-top: 10px;">
            <h1 style="margin: 0; color: white; font-weight:700; font-size:28px;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.9; margin-top: 8px; font-size: 15px; max-width: 700px;">
                Central administrative hub optimized for real-time classroom updates, digital asset access, performance management, and direct administrative escalation pathways.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h4 style="color:#64748b; margin:0; font-size:14px;">Total Cohort</h4><h1 style="color: #2563eb; margin:8px 0 0 0; font-weight:700;">1,250</h1></div>',
