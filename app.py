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
col_logo, col_title = st.columns([1, 11])
with col_title:
    st.markdown("<h2 style='margin: 0; color: #1e3a8a; font-weight:700;'>🎓 Academic Student Portal</h2>", unsafe_allow_html=True)
    st.markdown(f"Verification Tier: B.Sc Undergraduate • Helpdesk: <a href='mailto:{ADMIN_EMAIL}'>{ADMIN_EMAIL}</a>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 3. TOP TABS NAVIGATION (Hides Sidebar for easier access) ---
tabs = st.tabs(
