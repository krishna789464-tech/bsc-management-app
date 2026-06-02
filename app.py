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
    # Open the image using PIL for better compatibility with page_icon
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

# Custom Styling for App and Components
st.markdown("""
    <style>
    /* App background */
    .stApp { background-color: #f4f7f6; }
    
    /* Custom cards */
    .main-card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; }
    
    /* Professional Sidebar adjustments */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 10px;
    }
    .sidebar-meta {
        font-size: 13px;
        color: #4b5563;
        background-color: #f3f4f6;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
    }
    .sidebar-meta strong {
        color: #1f2937;
    }
    
    /* --- REMOVE GITHUB & STREAMLIT HEADER ELEMENTS --- */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# --- SECURE TARGET CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"

# --- 2. PROFESSIONAL SIDEBAR NAVIGATION ---
# Top Logo Section
if logo_exists and app_logo:
    st.logo(LOGO_PATH) 
else:
    st.sidebar.markdown("<h2 style='margin-top: 0; color: #2563eb;'>🎓 Portal</h2>", unsafe_allow_html=True)

# System / Meta Info Block
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-meta">
        <strong>🏫 Academic System</strong><br>
        <span style="opacity: 0.85;">Role: Student Access</span><br>
