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
    
    /* --- FIXED: REMOVE GITHUB & STREAMLIT ELEMENTS SAFELY --- */
    /* This hides the top-right menus (GitHub, Deploy, MainMenu) without destroying the sidebar toggle button */
    div[data-testid="stAppDeployButton"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    footer { visibility: hidden !important; }
    
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
            <h1 style="
